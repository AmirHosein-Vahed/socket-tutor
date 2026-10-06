import socket
import threading

def receive(sock):
    # Runs in a background thread so receiving doesn't block typing
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode(), end="")
        except OSError:
            break

s = socket.socket()
s.connect(("127.0.0.1", 5000))
threading.Thread(target=receive, args=(s,), daemon=True).start()

while True:
    msg = input()
    if msg == "exit":
        break
    s.sendall(msg.encode())
s.close()