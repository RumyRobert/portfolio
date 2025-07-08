import subprocess

import nmap
# from pysnmp.hlapi import *


import db_handler
import results

nm = nmap.PortScanner()


def scan_host(target_ip):
    nm.scan(target_ip, arguments='-p 1-65535')  # scan all ports from 1 to 65535

    test_result = []

    for host in nm.all_hosts():
        test_result.append("-- -- Host: " + host)
        for proto in nm[host].all_protocols():
            test_result.append("-- Protocol: " + proto)

            ports = sorted(nm[host][proto].keys())
            for port in ports:
                state = nm[host][proto][port]['state']
                test_result.append("Port: " + str(port) + " State: " + str(state))
    return test_result


def discover_hosts(target_network):
    nm.scan(hosts=target_network, arguments='-sn')  # discover all ip addresses in the network

    test_result = []

    print("started discover")

    test_result.append("-- Discovered Hosts:")
    for host in nm.all_hosts():
        print("discovered: " + host)
        test_result.append(str(host))
        try:
            results.addDevice(results.data["Scans"][0]["id"], None, None, host)
        except:
            results.addDevice(results.data["Scans"][0]["id"], None, None, host)

    return test_result

# def get_snmp_info(ip_address, community, oid):
#     print(ip_address)
#     iterator = getCmd(SnmpEngine(),
#                       CommunityData(community),
#                       UdpTransportTarget((ip_address, 161)),
#                       ContextData(),
#                       ObjectType(ObjectIdentity(oid)))
#
#     error_indication, error_status, error_index, var_binds = next(iterator)
#
#     if error_indication:
#         print(error_indication)
#         return None
#     elif error_status:
#         print('%s at %s' % (error_status.prettyPrint(),
#                             error_index and var_binds[int(error_index) - 1][0] or '?'))
#         return None
#     else:
#         for varBind in var_binds:
#             return varBind[1].prettyPrint()

def run_zgrab2_scan():

    print("started zgrab")

    zgrab2_command = ["./zgrab2/zgrab2", "siemens", "-f", "ip_range.txt"]

    # Execute the zgrab2 command
    try:
        result = subprocess.run(zgrab2_command, capture_output=True, text=True, check=True)
        # Capture the output of the scan
        output = result.stdout
        # Process the output as needed
        process_output(output)
    except subprocess.CalledProcessError as e:
        print("Error running zgrab2:", e)

def process_output(output):
    print("process output")
    print(output)
    results.process_json_output(output)

def complete_network_scan(target_network):
    print("complete network scan")
    port_id = 0
    nm.scan(hosts=target_network, arguments='-sn', timeout=300)  # discover all ip addresses in the network
    print("started complete network scan")
    # db_handler.setMaxDeviceID()
    temp_device_id = 0
    # discovered_hosts = []
    with open('ip_range.txt', 'w') as f:
        print("write in file")

        for host in nm.all_hosts():
            temp_device_id = temp_device_id+1
            # discovered_hosts.append(str(host))
            print("write: " + host)
            f.write(host + '\n')
            print("starting scan: " + host)
            nm.scan(host, arguments='-O -sV')
            print("finihed scan: " + host)

            try:
                results.data["Devices"].append({
                    "id": temp_device_id,
                    "scan_id": db_handler.scan_max_id,
                    "device_type": None,
                    "device_firmware": None,
                    "ip_address": host
                  })
            except:
                results.data["Devices"].append({
                    "id": temp_device_id,
                    "scan_id": None,
                    "device_type": None,
                    "device_firmware": None,
                    "ip_address": None
                })
                results.data["Devices"][-1]["scan_id"] =db_handler.scan_max_id
                results.data["Devices"][-1]["device_type"] = None
                try:
                    results.data["Devices"][-1]["device_firmware"] = None
                except:
                    results.data["Devices"][-1]["device_firmware"] = None
                results.data["Devices"][-1]["ip_address"] = host

                for proto in nm[host].all_protocols():
                    ports = sorted(nm[host][proto].keys())
                    for port in ports:
                        port_id += 1
                        results.data["OpenPorts"].append({
                          "id": port_id,
                          "device_id": temp_device_id,
                          "port_number": port
                        })

            db_handler.device_max_id += 1
            # for device in results.data["Devices"]:
            # try:
            #     # print(get_snmp_info(device["ip_address"], "public", '1.3.6.1.2.1.1.1.0')
            #     print(get_snmp_info(host, "public", '1.3.6.1.2.1.1.1.0'))
            #
            #       # OID for system description
            # except:
            #     print("Error: SNMP scan did not complete for device: " + host)
    print("calling zgrab scan")
    run_zgrab2_scan()




