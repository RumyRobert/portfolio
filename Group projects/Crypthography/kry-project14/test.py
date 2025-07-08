from datetime import datetime

import db_handler
import main
print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
main.connection.close()