import asyncio

async def receive(reader):
    while True:
        data = await reader.readline()
        if not data:
            print("Server closed the connection. Press Enter to exit.")
            break
        print(data.decode(), end="")

async def send(writer):
    while True:
        line = await asyncio.to_thread(input)     # Run blocking input() in a worker thread
        writer.write((line + "\n").encode())
        await writer.drain()
        if line == "/quit":
            break

async def main():
    reader, writer = await asyncio.open_connection("127.0.0.1", 5000)

    recv_task = asyncio.create_task(receive(reader))
    send_task = asyncio.create_task(send(writer))

    # Stop as soon as either side finishes
    done, pending = await asyncio.wait(
        {recv_task, send_task}, return_when=asyncio.FIRST_COMPLETED
    )
    for t in pending:
        t.cancel()

    writer.close()
    await writer.wait_closed()

asyncio.run(main())