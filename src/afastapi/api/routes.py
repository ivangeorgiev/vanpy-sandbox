import asyncio
import time

from fastapi import APIRouter

SLEEP_SECONDS = 10

router = APIRouter()

@router.get("/hello-sync/", tags=["hello"])
async def hello_sync():
    time.sleep(SLEEP_SECONDS)
    return "Hello, World! (sync)"

@router.get("/hello-to-thread/", tags=["hello"])
async def hello_tothread():
    start_time = time.time()
    await asyncio.to_thread(time.sleep, SLEEP_SECONDS)
    print(f"to_thread sleep took {time.time() - start_time:.2f} seconds")
    return "Hello, World! (to_thread)"

@router.get("/hello-async/", tags=["hello"])
async def hello_async():
    await asyncio.sleep(SLEEP_SECONDS)
    return "Hello, World! (async)"



