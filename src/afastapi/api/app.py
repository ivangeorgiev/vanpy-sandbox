import asyncio
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, FastAPI

from .routes import router as api_router

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=500)

app.include_router(api_router, prefix="/api")

@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    loop.set_default_executor(executor)
    app.state.threadpool_executor = executor


@app.on_event("shutdown")
async def shutdown():
    executor.shutdown(wait=True)
