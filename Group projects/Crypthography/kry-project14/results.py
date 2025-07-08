import json
from datetime import datetime

data = {}

data["Scans"] = []
data["Devices"] = []
data["OpenPorts"] = []
data["Vulnerabilities"] = []

def addScan(timestamp):

  data["Scans"].append({
    "id": 0,
    "timestamp": timestamp,
  })

def addDevice(scan_id, device_type, device_firmware, ip_address):

  data["Devices"].append({
    "id": 0,
    "scan_id": scan_id,
    "device_type": device_type,
    "device_firmware": device_firmware,
    "ip_address": ip_address
  })

# data["OpenPorts"].append({
#   "id": 0,
#   "device_id": 0,
#   "port_number": 0
# })
#
# data["Vulnerabilities"].append({
#   "id": 0,
#   "device_id": 0,
#   "name": "None",
#   "type": "None",
#   "CVSS": 0.0,
#   "reference": "None"
# })

def process_json_output(output):
  # Split the output into individual JSON objects
  output_lines = output.strip().split('\n')
  temp_device_id = 0
  # Process each JSON object
  for line in output_lines:
    temp_device_id = temp_device_id + 1
    # Remove invalid characters
    cleaned_line = ''.join(char for char in line if char.isprintable())
    # Parse cleaned JSON
    try:
      data = json.loads(cleaned_line)
      status = data['data']['siemens']['status']
      # Check if status is not "connection-timeout"
      if status != "connection-timeout": # change to success
        ip = data['ip']
        timestamp = datetime.fromisoformat(data['data']['siemens']['timestamp']).strftime("%Y-%m-%d %H:%M:%S")

        if 'result' in data['data']['siemens']:
          result = data['data']['siemens']['result']
          serial_number = result.get('serial_number', 'N/A')
          module_type = result.get('module_type', 'N/A')
          firmware = result.get('firmware', 'N/A')

          for device in data["Devices"]:
            if device["id"] == temp_device_id:
              device["id"] = serial_number
              device["device_type"] = module_type
              device["device_firmware"] = firmware
              break
          for port in data["OpenPorts"]:
            if port["device_id"] == temp_device_id:
              port["device_id"] = serial_number
              break

          # Print out the extracted information
          print("IP:", ip)
          print("Timestamp:", timestamp)
          print("Serial Number:", serial_number)
          print("Module Type:", module_type)
          print("Firmware:", firmware)
          print()  # Add a newline for better readability between entries
      else:
        print(f"Skipping IP {data['ip']} due to connection timeout.")
    except json.JSONDecodeError as e:
      print("Error decoding JSON:", e)
      print("Invalid JSON data:", cleaned_line)


def printResults():
  result = json.dumps(data, indent=4)
  print(result)
  return result

def cleanResults():
  data.clear()
  data["Scans"] = []
  data["Devices"] = []
  data["OpenPorts"] = []
  data["Vulnerabilities"] = []