from pysnmp.hlapi import *

def get_snmp_info(ip_address, community, oid):
    iterator = getCmd(SnmpEngine(),
                      CommunityData(community),
                      UdpTransportTarget((ip_address, 161)),
                      ContextData(),
                      ObjectType(ObjectIdentity(oid)))

    error_indication, error_status, error_index, var_binds = next(iterator)

    if error_indication:
        print(error_indication)
        return None
    elif error_status:
        print('%s at %s' % (error_status.prettyPrint(),
                            error_index and var_binds[int(error_index) - 1][0] or '?'))
        return None
    else:
        for varBind in var_binds:
            return varBind[1].prettyPrint()

# Example usage
ip_address = '192.168.211.1'  # Replace with your SNMP device IP
community = 'public'  # Replace with your SNMP community string
sys_descr_oid = '1.3.6.1.2.1.1.1.0'  # OID for system description
sys_uptime_oid = '1.3.6.1.2.1.1.3.0'  # OID for system uptime

sys_descr = get_snmp_info(ip_address, community, sys_descr_oid)
sys_uptime = get_snmp_info(ip_address, community, sys_uptime_oid)

print("System Description:", sys_descr)
print("System Uptime:", sys_uptime)
