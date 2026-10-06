import socket

with socket.socket() as client:
    client.connect(("127.0.0.1", 5000))
    while True:
        msg = input("Message (type exit to quit): ")
        if msg == "exit":
            break
        client.sendall(msg.encode())
        print("Reply:", client.recv(1024).decode())