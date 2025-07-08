from datetime import datetime

import mysql.connector

import main
import results

# host = "sql11.freemysqlhosting.net"
# user = "sql11689974"
# password = "x9RMRjnASB"
# database = "sql11689974"

# connection = mysql.connector.connect(
#     host=host,
#     user=user,
#     password=password,
#     database=database
# )





# cursor = connection.cursor()

# cursor.execute("SELECT * FROM sql11689974.Scans")
# result = cursor.fetchall()
#
# def printRestults():
#     print(result)


def setMaxScanID_inResults():
    cursor = main.connection.cursor()

    cursor.execute("SELECT MAX(id) FROM sql11689974.Scans")

    scan_max_id = cursor.fetchone()[0] + 1
    scan_max_id = scan_max_id if scan_max_id is not None else 0
    # results.data["Scans"][0]["id"] = scan_max_id

    cursor.close()
    return scan_max_id

def setMaxDeviceID():
    cursor = main.connection.cursor()

    cursor.execute("SELECT MAX(id) FROM sql11689974.Devices")

    device_max_id = cursor.fetchone()[0] + 1
    device_max_id = device_max_id if device_max_id is not None else 0

    cursor.close()

    return device_max_id


def uploadResults_toDatabase():
    cursor = main.connection.cursor()
    cursor.execute("INSERT INTO sql11689974.Scans (timestamp) VALUES (%s)", (results.data["Scans"][0]["timestamp"],))
    main.connection.commit()

    for device in results.data["Devices"]:
        cursor.execute("INSERT INTO sql11689974.Devices (scan_id, device_type, device_firmware ip_address) VALUES (%s, %s, %s, %s, %s)",
                       (device["scan_id"], device["device_type"], device["device_firmware"], device["ip_address"]))
        main.connection.commit()


    cursor.close()

    # connection.close()

def uploadFullScanResults_toDatabase():
    cursor = main.connection.cursor()
    cursor.execute("INSERT INTO sql11689974.Scans (timestamp) VALUES (%s)", (results.data["Scans"][0]["timestamp"],))
    main.connection.commit()

    for device in results.data["Devices"]:
        cursor.execute("INSERT INTO sql11689974.Devices (scan_id, device_type, device_firmware, ip_address) VALUES (%s, %s, %s, %s, %s)",
                       (device["scan_id"], device["device_type"], device["device_firmware"], device["ip_address"]))
        main.connection.commit()

    for port in results.data["OpenPorts"]:
        cursor.execute("INSERT INTO sql11689974.OpenPorts (device_id, port_number) VALUES (%s, %s)", (port["device_id"], port["port_number"]))
        main.connection.commit()

    cursor.close()

    # connection.close()

scan_max_id = setMaxScanID_inResults()
device_max_id = setMaxDeviceID()