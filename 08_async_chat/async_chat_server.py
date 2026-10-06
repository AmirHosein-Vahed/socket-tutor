import asyncio

clients = {}   # writer -> username

async def broadcast(message, exclude=None):
    # list(...) makes a copy: the dict may change while we await inside the loop
    for w in list(clients):
        if w is exclude:
            continue
        try:
            w.write(message.encode())
            await w.drain()
        except ConnectionError:
            clients.pop(w, None)

async def handle(reader, writer):
    writer.write(b"Enter your name: ")
    await writer.drain()
    name = (await reader.readline()).decode().strip()

    if not name or name in clients.values():
        writer.write(b"Invalid or already taken name\n")
        await writer.drain()
        writer.close()
        return

    clients[writer] = name
    print(f"[+] {name} joined")
    await broadcast(f"* {name} joined\n", exclude=writer)

    try:
        while line := await reader.readline():
            text = line.decode().strip()
            if text == "/quit":
                break
            elif text == "/list":
                writer.write(("Online: " + ", ".join(clients.values()) + "\n").encode())
                await writer.drain()
            elif text:
                await broadcast(f"{name}: {text}\n", exclude=writer)
    except ConnectionError:
        pass
    finally:
        clients.pop(writer, None)
        writer.close()
        print(f"[-] {name} left")
        await broadcast(f"* {name} left\n")

async def main():
    server = await asyncio.start_server(handle, "0.0.0.0", 5000)
    print("Chat server started on port 5000")
    async with server:
        await server.serve_forever()

asyncio.run(main())