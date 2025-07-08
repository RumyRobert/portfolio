import subprocess

def scan_nvme_devices():
    try:
        output = subprocess.check_output(["nvme", "list"], text=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print("Error:", e)

if __name__ == "__main__":
    scan_nvme_devices()
