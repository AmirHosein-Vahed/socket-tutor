import asyncio

async def worker(name, delay):
    print(f"{name} started")
    await asyncio.sleep(delay)        # Yields control to the event loop (non-blocking)
    print(f"{name} finished after {delay}s")
    return name

async def main():
    # Run three coroutines concurrently and collect their results
    results = await asyncio.gather(
        worker("A", 2),
        worker("B", 1),
        worker("C", 3),
    )
    print("Results:", results)

asyncio.run(main())                   # Creates the event loop, runs main(), closes the loop