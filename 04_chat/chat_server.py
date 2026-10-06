import socket
import threading

clients = []
lock = threading.Lock()   # Protects the shared clients list

def broadcast(message, sender=None):
    with lock:
        for c in clients[:]:          # Iterate over a copy of the list
            if c is not sender:
                try:
                    c.sendall(message)
                except OSError:
                    clients.remove(c) # Remove dead connections

def handle(conn, addr):
    with lock:
        clients.append(conn)
    broadcast(f"* {addr[1]} joined\n".encode(), conn)
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            broadcast(f"{addr[1]}: ".encode() + data, conn)
    finally:
        with lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()
        broadcast(f"* {addr[1]} left\n".encode())

with socket.socket() as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 5000))
    server.listen()
    print("Chat server started")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle, args=(conn, addr), daemon=True).start()