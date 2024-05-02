from fastapi import (
    Depends,
    WebSocketDisconnect,
)
from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket

from punq import Container

from infra.websockets.managers import BaseConnectionManager
from logic.init import init_container

router = APIRouter(tags=["chats"])


@router.websocket("/{chat_oid}/")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_oid: str,
    container: Container = Depends(init_container),
):
    connection_manager: BaseConnectionManager = container.resolve(BaseConnectionManager)
    await connection_manager.accept_connection(websocket=websocket, key=chat_oid)

    await websocket.send_text("You are now connected!")

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        await connection_manager.remove_connection(websocket=websocket, key=chat_oid)
