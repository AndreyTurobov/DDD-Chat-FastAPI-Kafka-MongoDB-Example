from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from starlette.websockets import (
    WebSocket,
    WebSocketDisconnect,
)

from punq import Container

from infra.websockets.managers import BaseConnectionManager
from logic.exceptions.messages import ChatNotFoundException
from logic.init import init_container
from logic.mediator.base import Mediator
from logic.queries.messages import GetChatDetailQuery

router = APIRouter(tags=["chats"])


@router.websocket("/{chat_oid}/")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_oid: str,
    container: Container = Depends(init_container),
) -> None:
    connection_manager: BaseConnectionManager = container.resolve(BaseConnectionManager)
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_query(GetChatDetailQuery(chat_oid=chat_oid))
    except ChatNotFoundException as error:
        await websocket.accept()
        await websocket.send_json(data={"error": error.message})
        await websocket.close()
        return

    await connection_manager.accept_connection(websocket=websocket, key=chat_oid)

    await websocket.send_text("You are now connected!")

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        await connection_manager.remove_connection(websocket=websocket, key=chat_oid)
