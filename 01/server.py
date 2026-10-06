import socket

# AF_INET = IPv4, SOCK_STREAM = TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    # Allow reusing the port immediately after the server restarts
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 5000))
    server.listen()
    print("Server is waiting for a connection...")
    conn, addr = server.accept()
    with conn:
        print("Connection from", addr)
        data = conn.recv(1024)
        print("Received:", data.decode("utf-8"))
        conn.sendall("Hello from server!".encode("utf-8"))

# import socket

# AF_INET = IPv4, SOCK_STREAM = TCP
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server.bind(("127.0.0.1", 5000))   # Bind the socket to an address and port
# server.listen()                     # Ready to accept incoming connections
# print("Server is waiting for a connection...")

# conn, addr = server.accept()        # Blocks until a client connects
# print("Connection from:", addr)

# data = conn.recv(1024)              # Receive up to 1024 bytes
# print("Received:", data.decode("utf-8"))

# conn.sendall("Hello from server!".encode("utf-8"))

# conn.close()
# server.close()