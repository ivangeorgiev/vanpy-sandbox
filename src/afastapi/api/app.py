import time
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from .routes import router as api_router

logger = logging.getLogger("uvicorn.error")

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# handler = logging.StreamHandler()
# formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
# handler.setFormatter(formatter)
# logger.addHandler(handler)

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=500)


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start
        msg = f"{request.method} {request.url.path} completed in {elapsed:.4f} seconds"
        logger.info(msg)
        response.headers["X-Process-Time"] = str(elapsed)
        return response


app.add_middleware(TimingMiddleware)

app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    loop.set_default_executor(executor)
    app.state.threadpool_executor = executor


@app.on_event("shutdown")
async def shutdown():
    executor.shutdown(wait=True)
