import socket
import struct
import time

print("Testing UDP Multicast discovery on Wi-Fi (192.168.12.108)...")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    sock.bind(("", 7400))
    # Join 239.255.0.1 on 192.168.12.108
    mreq = struct.pack("4s4s", socket.inet_aton("239.255.0.1"), socket.inet_aton("192.168.12.108"))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    print("Joined multicast group 239.255.0.1:7400 successfully.")
    
    sock.settimeout(3.0)
    start = time.time()
    packets = 0
    while time.time() - start < 3.0:
        try:
            data, addr = sock.recvfrom(65535)
            print(f"-> Received multicast packet from {addr}: {len(data)} bytes (header: {data[:4]})")
            packets += 1
            if packets >= 5:
                break
        except socket.timeout:
            break
    print(f"Total multicast packets received: {packets}")
except Exception as e:
    print(f"Error: {e}")
finally:
    sock.close()
