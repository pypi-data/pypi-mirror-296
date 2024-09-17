import asyncio

async def test_concurrent(name, fn, timeout=5):
    await asyncio.wait_for(fn(), timeout)
