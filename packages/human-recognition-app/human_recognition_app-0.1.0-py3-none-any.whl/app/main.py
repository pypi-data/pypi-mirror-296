import os
from contextlib import asynccontextmanager

from app.api.router import task_router
from app.database.client import DatabaseClient
from app.network.client import NetworkClient
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.gzip import GZipMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    await DatabaseClient().connect()
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    yield
    await DatabaseClient().disconnect()
    await NetworkClient().disconnect()


app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

app.add_middleware(GZipMiddleware)


app.include_router(task_router)
