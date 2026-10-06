import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(2)                        # Don't wait forever for a reply
s.sendto("Hello UDP".encode(), ("127.0.0.1", 6000))
try:
    data, _ = s.recvfrom(1024)
    print(data.decode())
except socket.timeout:
    print("No reply received (the packet may have been lost)")