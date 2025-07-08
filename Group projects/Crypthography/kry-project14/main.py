from datetime import datetime

import mysql.connector
from flask import Flask, render_template, request

import db_handler
import results
import scan
import cve_data_retrieve

app = Flask(__name__)

host = "sql11.freemysqlhosting.net"
user = "sql11689974"
password = "x9RMRjnASB"
database = "sql11689974"

connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

@app.route('/')
def home():

    return render_template('home.html')

@app.route('/execute_scan', methods = ['POST'])
def execute_scan():
    results.addScan(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    db_handler.setMaxScanID_inResults()
    if request.method == 'POST':
        target = request.form.get('target')
        if (target.__contains__('/')): #check if input was host or network address
            # result = scan.discover_hosts(target)
            result = results.printResults()
            scan.complete_network_scan(target)

        else:
            result = scan.scan_host(target)

        for device in results.data["Devices"]:
            device_firmware = device["device_firmware"]
            cve_data_retrieve.CVE_val(device_firmware)

        result = results.printResults()
        # db_handler.uploadResults_toDatabase()
        # db_handler.uploadFullScanResults_toDatabase()
        # db_handler.connection.close() #when data is uploadted, no need for this
        results.cleanResults()
        return render_template('scan_result.html', result = result)
    else:
        return "ERROR: Invalid request!"


if __name__ == '__main__':
    try:

        app.run(debug=True)
        connection.close()
    finally:
        connection.close()
