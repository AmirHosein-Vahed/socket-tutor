import socket

with socket.socket() as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 5000))
    server.listen()
    print("Waiting for a connection...")

    conn, addr = server.accept()
    with conn:
        print("Connected:", addr)
        while True:
            data = conn.recv(1024)
            if not data:          # b"" means the other side closed the connection
                print("Client disconnected")
                break
            print("Recieved:", data.decode('utf-8'))
            conn.sendall(data)    # Send the same data back (echo)