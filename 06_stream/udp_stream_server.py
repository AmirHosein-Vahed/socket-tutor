import socket
import time
import random

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("127.0.0.1", 6000))
s.settimeout(0.1)              # Short timeout so we can alternate between listening and sending
print("UDP stream server is ready on port 6000")

subscribers = set()            # Addresses of clients that asked for the stream
seq = 0                        # Sequence number, increases with every packet
INTERVAL = 0.5                 # Seconds between two numbers
last_sent = time.time()

while True:
    # --- Part 1: check for control messages from clients ---
    try:
        data, addr = s.recvfrom(1024)
        msg = data.decode().strip()
        if msg == "SUBSCRIBE":
            subscribers.add(addr)
            print("Subscribed:", addr)
        elif msg == "UNSUBSCRIBE":
            subscribers.discard(addr)
            print("Unsubscribed:", addr)
    except socket.timeout:
        pass                   # Nothing received, that's fine
    except ConnectionResetError:
        pass                   # Windows may raise this when a client port is closed

    # --- Part 2: send the next number if it's time ---
    if time.time() - last_sent >= INTERVAL:
        value = random.randint(0, 100)
        packet = f"{seq},{value}".encode()      # Format: "sequence,value"
        for client_addr in subscribers:
            s.sendto(packet, client_addr)
        if subscribers:
            print(f"Sent seq={seq} value={value} to {len(subscribers)} client(s)")
        seq += 1
        last_sent = time.time()