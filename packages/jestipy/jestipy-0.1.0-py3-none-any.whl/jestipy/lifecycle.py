import asyncio

_lifecycle_hooks = {
    "beforeAll": None,
    "afterAll": None,
    "beforeEach": None,
    "afterEach": None
}

async def run_with_timeout(fn, timeout):
    try:
        if asyncio.iscoroutinefunction(fn):
            await asyncio.wait_for(fn(), timeout)
        else:
            await asyncio.wait_for(asyncio.to_thread(fn), timeout)
    except asyncio.TimeoutError:
        raise TimeoutError(f"Test exceeded timeout of {timeout} seconds")

async def run_lifecycle_hooks(hook_name):
    hook = _lifecycle_hooks.get(hook_name)
    if hook:
        print(f"Running {hook_name} hook")
        await run_with_timeout(hook, 5) 
