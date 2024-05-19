from abc import (
    ABC,
    abstractmethod,
)
import asyncio
from collections import defaultdict
from dataclasses import (
    dataclass,
    field,
)

from starlette.websockets import WebSocket


@dataclass
class BaseConnectionManager(ABC):
    connections_map: dict[str, list[WebSocket]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    @abstractmethod
    async def accept_connection(self, websocket: WebSocket, key: str) -> None: ...

    @abstractmethod
    async def remove_connection(self, websocket: WebSocket, key: str) -> None: ...

    @abstractmethod
    async def send_all(self, key: str, bytes_: bytes) -> None: ...

    @abstractmethod
    async def disconnect_all(self, key: str) -> None: ...


@dataclass
class ConnectionManager(BaseConnectionManager):
    lock_map: dict[str, asyncio.Lock] = field(
        default_factory=dict,
    )

    async def accept_connection(self, websocket: WebSocket, key: str) -> None:
        await websocket.accept()

        if key not in self.lock_map:
            self.lock_map[key] = asyncio.Lock()

        async with self.lock_map[key]:
            # TODO: check if chat in delete process
            self.connections_map[key].append(websocket)

    async def remove_connection(self, websocket: WebSocket, key: str) -> None:
        async with self.lock_map[key]:
            self.connections_map[key].remove(websocket)

    async def send_all(self, key: str, bytes_: bytes) -> None:
        for websocket in self.connections_map[key]:
            await websocket.send_bytes(bytes_)

    async def disconnect_all(self, key: str) -> None:
        async with self.lock_map[key]:
            for websocket in self.connections_map[key]:
                await websocket.send_json(
                    {"message": "Chat was deleted"},
                )
                await websocket.close()
