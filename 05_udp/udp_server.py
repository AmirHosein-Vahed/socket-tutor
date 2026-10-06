import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # SOCK_DGRAM = UDP
s.bind(("127.0.0.1", 6000))
print("UDP server is ready")

while True:
    data, addr = s.recvfrom(1024)     # Returns the data and the sender's address
    print(addr, data.decode())
    s.sendto(b"received", addr)       # Reply directly to the sender