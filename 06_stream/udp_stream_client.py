import socket

SERVER = ("127.0.0.1", 6000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(3)                         # If nothing arrives for 3 seconds, assume the stream stopped

s.sendto(b"SUBSCRIBE", SERVER)          # Introduce ourselves to the server
print("Subscribed. Waiting for numbers... (Ctrl+C to stop)")

expected_seq = None                     # The next sequence number we expect to see
received = 0
lost = 0

try:
    while True:
        try:
            data, _ = s.recvfrom(1024)
        except socket.timeout:
            print("No data for 3 seconds, stopping.")
            break

        seq_str, value_str = data.decode().split(",")
        seq, value = int(seq_str), int(value_str)

        # Detect gaps in the sequence (lost packets)
        if expected_seq is not None and seq > expected_seq:
            gap = seq - expected_seq
            lost += gap
            print(f"  ! Lost {gap} packet(s) before seq={seq}")
        elif expected_seq is not None and seq < expected_seq:
            print(f"  ! Out-of-order or duplicate packet seq={seq}, ignored")
            continue

        expected_seq = seq + 1
        received += 1
        print(f"seq={seq:4d} | value={value:3d} | {'#' * (value // 5)}")   # Simple bar display

except KeyboardInterrupt:
    pass
finally:
    s.sendto(b"UNSUBSCRIBE", SERVER)    # Politely leave the stream
    s.close()
    print(f"\nReceived: {received}, Lost: {lost}")