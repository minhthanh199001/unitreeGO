import socket
from concurrent.futures import ThreadPoolExecutor

target = "192.168.12.1"
print(f"Scanning {target} for open ports...")

def check_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.3)
    res = s.connect_ex((target, port))
    s.close()
    if res == 0:
        return port
    return None

# Check interesting ports
ports_to_check = [
    21, 22, 23, 53, 80, 443, 554, 1883, 3000, 5000, 7400, 7401, 7402, 7410, 7411,
    8000, 8080, 8081, 8082, 8088, 8090, 8443, 8554, 8888, 9000, 9090, 9991, 9992,
    9999, 10000, 10001, 10002, 10003, 10004, 30000
]
# Also scan 8000-8100 and 9900-10000
ports_to_check += list(range(8000, 8100))
ports_to_check += list(range(9980, 10010))
ports_to_check = sorted(list(set(ports_to_check)))

open_ports = []
with ThreadPoolExecutor(max_workers=50) as ex:
    for port in ex.map(check_port, ports_to_check):
        if port:
            open_ports.append(port)

print("Open TCP ports:", open_ports)
