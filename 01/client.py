import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(("127.0.0.1", 5000))

    client.sendall("Hello from client!".encode("utf-8"))
    reply = client.recv(1024)
    print("Reply:", reply.decode("utf-8"))
