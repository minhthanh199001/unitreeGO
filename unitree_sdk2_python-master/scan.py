import socket

target = "192.168.12.1"
print(f"Scanning {target}...")
for port in [22, 53, 80, 443, 8080, 8081, 8082, 9999, 5000, 3000]:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    r = s.connect_ex((target, port))
    if r == 0:
        print(f"Port {port}: OPEN (TCP)")
    s.close()
