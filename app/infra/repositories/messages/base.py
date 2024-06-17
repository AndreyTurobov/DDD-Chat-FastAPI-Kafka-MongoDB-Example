from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import Iterable
from dataclasses import dataclass

from domain.entities.messages import (
    Chat,
    Message,
)
from infra.repositories.filters.messages import GetMessagesFilters


@dataclass
class BaseChatsRepository(ABC):
    @abstractmethod
    async def check_chat_exists_by_title(self, title: str) -> bool: ...

    @abstractmethod
    async def get_chat_by_oid(self, oid: str) -> Chat | None: ...

    @abstractmethod
    async def add_chat(self, chat: Chat) -> None: ...

    @abstractmethod
    async def get_all_chats(
        self, filters: GetMessagesFilters
    ) -> tuple[Iterable[Chat], int]: ...

    @abstractmethod
    async def delete_chat_by_oid(self, chat_oid: str) -> None: ...

    @abstractmethod
    async def add_telegram_listener(
        self, chat_oid: str, telegram_chat_id: str
    ) -> None: ...


@dataclass
class BaseMessagesRepository(ABC):
    @abstractmethod
    async def add_message(self, message: Message) -> None: ...

    # @abstractmethod
    # async def get_messages_by_chat_oid(self, chat_oid: str) -> Iterable[Message]:
    #     ...
    #
    # @abstractmethod
    # async def get_messages_by_text(self, text: str) -> Iterable[Message]:
    #     ...

    @abstractmethod
    async def get_messages(
        self,
        chat_oid: str,
        filters: GetMessagesFilters,
    ) -> tuple[Iterable[Message], int]: ...
