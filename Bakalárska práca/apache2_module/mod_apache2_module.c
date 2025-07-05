#include <apr_strings.h>
#include <apr_network_io.h>
#include <apr_hash.h>
#include <apr_time.h>
#include <time.h>
#include <stdio.h>
#include <httpd.h>
#include <http_config.h>
#include <http_log.h>
#include <apr.h>
#include <apr_pools.h>
#include <scoreboard.h>
#include <mpm_common.h>


module AP_MODULE_DECLARE_DATA apache20_module;


#define MAX_HITS        150  //Maximum number of times a user can connect within an interval without being blocked
#define INTERVAL        10  //a time interval which is used to calculate the rate of requests
#define BLOCKING_PERIOD 60  //value in seconds for which the user gets timed out upon exceeding the set limit within a certain amount of time

#define ANTILORIS_COUNTER_TYPE_COUNT 2
#define ANTILORIS_READ_COUNT_INDEX 0
#define ANTILORIS_WRITE_COUNT_INDEX 1


#define MAX_CONN   10  //maximum connections
#define MAX_READ   5   //maximum connections for reading
#define MAX_WRITE  5    //maximum connections for writing



static int blocking_period = BLOCKING_PERIOD;
static int maximum_hits = MAX_HITS; 
static int interval = INTERVAL;
static int server_limit, thread_limit;

static int total_limit = MAX_CONN;
static int write_limit = MAX_WRITE;
static int read_limit  = MAX_READ;


struct requester{
    char ip[21];
    time_t timestamp;
    int count;
    time_t last_data_time;
};

typedef struct {
    int child_num;
    int thread_num;
} sb_handle;

struct requester *hits[2048];  //Number of times the user connected to the server


const char *whitelisted_addresses[1024][15] = {{"127.0.0.1"}};

static int access_checker(request_rec *r);
void insert(char ip[], time_t timestamp);
struct requester *create(long size, apr_pool_t *pool);
int is_whitelisted(const char *ip);
struct requester *find_user(const char *ip);
int clear_mem(struct requester **hits);
static void register_hooks(apr_pool_t *p);
static apr_status_t destroy_list(void *data, apr_pool_t *p);
static int _reached_ip_con_limit(short *ip_counts, conn_rec *c);

static int access_checker(request_rec *r)
{   // This function first checks if the IP address of the requester is whitelised, if he is not, the rate of requests is calculated and if it exceeds the limit, the user gets blacklisted 
    struct requester *user = NULL;
    time_t t = time(NULL);
    int ret = OK;
    if(is_whitelisted(r->connection->client_ip))    //Checking if the user is whitelisted, IF yes, without any controlling, the user gains access
    {
        ap_log_rerror(APLOG_MARK, APLOG_ERR,0,r,"User %s is whitelisted.", r->connection->client_ip);
        return OK;
    }
    if(user!=NULL && t-user->timestamp<blocking_period){    //Looking for the user in the blacklisted addresses, IF found AND the blocking period did not expire, deny access
        user->timestamp = time(NULL);
        return HTTP_FORBIDDEN;
    }
    else
    {
        user = find_user(r->connection->client_ip);
        if(user!=NULL)
        {      
            if(t-user->timestamp<interval && user->count>=maximum_hits)  //check amount of hits within an interval, has site been hit too much?
            {    
                ret = HTTP_FORBIDDEN;
                ap_log_rerror(APLOG_MARK, APLOG_ERR,0,r,"Site has been hit too much by: %s/ %d", r->connection->client_ip, user->count);
            }
            else if(t-user->timestamp>=interval) 
            {
                user->count=0;
            }
            user->timestamp = t;
            user->count++;
        }
        else
        {
            insert(r->connection->client_ip, t);
            user = find_user(r->connection->client_ip);
        }
    }
    if(ret==HTTP_FORBIDDEN ){
        ap_log_rerror(APLOG_MARK, APLOG_ERR, 0, r,"Client denied by server configuration: %s",r->filename);
    }
    return ret;
}

static int pre_conn(conn_rec *conn){
    char* client_ip = conn->client_ip;
    short ip_counts[ANTILORIS_COUNTER_TYPE_COUNT] = {0, 0};
#if AP_MODULE_MAGIC_AT_LEAST(20110605, 2)
    /* get the socket descriptor */
    apr_socket_t *csd = ap_get_conn_socket(conn);
#endif
    worker_score *ws_record;
    sb_handle *sbh = conn->sbh;

    ws_record = &ap_scoreboard_image->servers[sbh->child_num][sbh->thread_num];
    apr_cpystrn(ws_record->client, client_ip, 21);


for (int i = 0; i < server_limit; ++i)  //iterates over the server workers
    {
        for (int j = 0; j < thread_limit; ++j) //iterates over the threads
        {
            #if AP_MODULE_MAGIC_AT_LEAST(20071023, 0)
                ws_record = ap_get_scoreboard_worker_from_indexes(i, j);
            #else
                ws_record = ap_get_scoreboard_worker(i, j);
            #endif

            switch (ws_record->status) //compares the client ip and with the client field of ws_record, if they match, it increments the number of connections of the user based on whether the connection is for reading or writing
                {
                case SERVER_BUSY_READ:
                    /* READING STATE */
                    if (strcmp(client_ip, ws_record->client) == 0)
                        ip_counts[ANTILORIS_READ_COUNT_INDEX]++;
                    break;
                case SERVER_BUSY_WRITE:
                    /* WRITING STATE */
                    if (strcmp(client_ip, ws_record->client) == 0)
                        ip_counts[ANTILORIS_WRITE_COUNT_INDEX]++;
                    break;
                default:
                    break;
                }

        }
    }

    if (_reached_ip_con_limit(ip_counts, conn)) {   //if the limit is reached, the server returns HTTP_FORBIDDEN to the requester

        ap_log_cerror(APLOG_MARK, APLOG_ERR, 0, conn, "Connection limit exceeded by user: %s!", client_ip);
        return HTTP_FORBIDDEN;
    }
    return DECLINED;
}

static int _reached_ip_con_limit(short *ip_counts, conn_rec *conn){ //checks the connection values of the requester whether they reached the limit
    int ret=0;
    signed short ip_total_count = 0;
    for (int i = 0; i < ANTILORIS_COUNTER_TYPE_COUNT; i++){
        ip_total_count += ip_counts[i];
    }
   
    if(ip_total_count>total_limit){
      ap_log_cerror(APLOG_MARK, APLOG_WARNING, 0, conn, "TOTAL CONNECTION LIMIT EXCEEDED");
      ret = 1;  
    }
    if(ip_counts[ANTILORIS_READ_COUNT_INDEX]>read_limit){
        ap_log_cerror(APLOG_MARK, APLOG_WARNING, 0, conn, "CONNECTION LIMIT FOR READING EXCEEDED"); 
        ret = 1;
    }
    if (ip_counts[ANTILORIS_WRITE_COUNT_INDEX]>write_limit)
    {
        ap_log_cerror(APLOG_MARK, APLOG_WARNING, 0, conn, "CONNECTION LIMIT FOR WRITING EXCEEDED"); 
        ret = 1;
    }

    return ret;
}

static int post_config(apr_pool_t *p,server_rec *s) {
    ap_mpm_query(AP_MPMQ_HARD_LIMIT_THREADS, &thread_limit);
    ap_mpm_query(AP_MPMQ_HARD_LIMIT_DAEMONS, &server_limit);
    return OK;
}



void insert(char ip[], time_t timestamp){   
    //inserting the user into the blacklisted addresses
    apr_pool_t *pool;
    apr_pool_create(&pool, NULL);
    struct requester *r = (struct requester *)apr_pcalloc(pool, sizeof(struct requester)); // Allocate memory for the new requester struct
    strcpy(r->ip, ip);
    r->timestamp = timestamp;
    r->count = 1;
    for(int i=0;i<2048;i++)
    {
        if(hits[i]==NULL)
            hits[i]=r;

            return;
    }
    apr_pool_destroy(pool);
    return;
}

struct requester *find_user(const char *ip){ 
    //searching for a user in access list
    struct requester *temp_user= NULL;
     for(int i=0;i<2048; i++)
    {
            if(hits[i]!=NULL && strcmp(hits[i]->ip,ip)==0){     
                temp_user = hits[i];
                return temp_user;
            }
    }
    return temp_user;
}

int is_whitelisted(const char* ip){  
    //checking if the user is part of the whitelisted addresses
    for(int i=0;i<1024;i++)
    {
        if(whitelisted_addresses[i][0]!='\0' && strcmp(ip, *whitelisted_addresses[i])==0)
        {
            return 1;
        }
    }
    return 0;
}


static apr_status_t destroy_list(void *data, apr_pool_t *p){ //clears the pool and frees memory allocated for the program
    for(int i=0; i<2048; i++){
        free(hits[i]);
    }
    apr_pool_clear(p);
    return APR_SUCCESS;
}

static void register_hooks(apr_pool_t *p){
    ap_hook_process_connection(pre_conn,NULL,NULL,APR_HOOK_FIRST);
    ap_hook_access_checker(access_checker,NULL,NULL,APR_HOOK_MIDDLE);
    apr_pool_cleanup_register(p,NULL,apr_pool_cleanup_null, destroy_list);
    ap_hook_post_config(post_config, NULL, NULL, APR_HOOK_MIDDLE);
}


module AP_MODULE_DECLARE_DATA apache2_module = {
    STANDARD20_MODULE_STUFF,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    register_hooks
};