from contextlib import asynccontextmanager

from fastapi.applications import FastAPI

from aiojobs._scheduler import Scheduler
from punq import Container

from application.api.lifespan import (
    close_message_broker,
    consume_in_background,
    init_message_broker,
)
from application.api.messages.handlers import router as message_router
from application.api.messages.websockets.messages import router as message_ws_router
from logic.init import init_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_message_broker()
    container: Container = init_container()
    scheduler: Scheduler = container.resolve(Scheduler)
    job = await scheduler.spawn(consume_in_background())
    yield
    await close_message_broker()
    await job.close()


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title="Simple FastAPI Kafka Chat",
        docs_url="/api/docs",
        description="A simple fastapi + kafka + DDD example",
        debug=True,
    )
    app.include_router(message_router, prefix="/chats")
    app.include_router(message_ws_router, prefix="/chats")

    return app
