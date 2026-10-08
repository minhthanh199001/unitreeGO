import socket
import struct

MCAST_GRP = '239.255.0.1'
MCAST_PORT = 7400

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))

mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

sock.settimeout(5.0)

print("Listening for DDS Multicast on 239.255.0.1:7400...")
try:
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received multicast from {addr}")
        break
except socket.timeout:
    print("No multicast packets received in 5 seconds.")
