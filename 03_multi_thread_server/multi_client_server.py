import socket
import threading

def handle_client(conn, addr):
    print(f"[+] {addr} connected")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(f"Echo: {data.decode()}".encode())
    print(f"[-] {addr} disconnected")

with socket.socket() as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 5000))     # 0.0.0.0 = listen on all network interfaces
    server.listen()
    print("Server is ready")
    while True:
        conn, addr = server.accept()
        # One thread per client; daemon threads exit with the main program
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()