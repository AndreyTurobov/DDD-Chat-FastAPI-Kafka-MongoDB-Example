from contextlib import asynccontextmanager

from fastapi import FastAPI

from application.api.lifespan import start_kafka, stop_kafka
from application.api.messages.handlers import router as message_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_kafka()
    yield
    await stop_kafka()


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title="Simple FastAPI Kafka Chat",
        docs_url="/api/docs",
        description="A simple fastapi + kafka + DDD example",
        debug=True,
    )
    app.include_router(message_router, prefix="/chat")

    return app
