import psutil
import subprocess
import time
import os
import socket

# Check for usb0 and if it has an IP
def usb0_check():
    for iface, addrs in psutil.net_if_addrs().items():
        if iface == 'usb0':
            has_ip = any(addr.address for addr in addrs if addr.family == socket.AF_INET)
            return not has_ip
    return False

# Ping to confirm pwnagotchi has connected 
def ping_pwnagotchi(host, timeout=2):
    try:
        result = subprocess.run(
            ['ping', '-c', '1', '-W', str(timeout), host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.returncode == 0
    except Exception as error:
        print(f"Ping error: {error}")
        return False
    

# Monitor for usb0 
def monitor():
    while True:
        if usb0_check():
            print("usb0 detected no IP. Running script")
            subprocess.run(['sudo', '/bin/bash', os.path.expanduser('~/linux_connection_share.sh')])
            time.sleep(5)  # wait for pwnagotchi to connect

            if ping_pwnagotchi("10.0.0.2"):
                print("Ping success, pwnagotchi connected")
            else:
                print("Ping failed, retrying")
        
        time.sleep(60)

if __name__ == "__main__":
    monitor()
