from datetime import datetime

from pydantic.main import BaseModel

from application.api.schemas import BaseQueryResponseSchema
from domain.entities.messages import (
    Chat,
    ChatListener,
    Message,
)


class CreateChatRequestSchema(BaseModel):
    title: str


class CreateChatResponseSchema(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> "CreateChatResponseSchema":
        return CreateChatResponseSchema(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
        )


class CreateMessageRequestSchema(BaseModel):
    text: str


class CreateMessageResponseSchema(BaseModel):
    text: str
    oid: str

    @classmethod
    def from_entity(cls, message: Message) -> "CreateMessageResponseSchema":
        return CreateMessageResponseSchema(
            text=message.text.as_generic_type(),
            oid=message.oid,
        )


class MessageDetailSchema(BaseModel):
    oid: str
    text: str
    created_at: datetime

    @classmethod
    def from_entity(cls, message: Message) -> "MessageDetailSchema":
        return MessageDetailSchema(
            oid=message.oid,
            text=message.text.as_generic_type(),
            created_at=message.created_at,
        )


class ChatDetailSchema(BaseModel):
    oid: str
    title: str
    created_at: datetime

    @classmethod
    def from_entity(cls, chat: Chat) -> "ChatDetailSchema":
        return ChatDetailSchema(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
            created_at=chat.created_at,
        )


class GetMessagesQueryResponseSchema(
    BaseQueryResponseSchema[list[MessageDetailSchema]]
): ...


class GetAllChatsQueryResponseSchema(
    BaseQueryResponseSchema[list[ChatDetailSchema]]
): ...


class AddTelegramListenerSchema(BaseModel):
    telegram_chat_id: str


class AddTelegramListenerResponseSchema(BaseModel):
    listener_id: str

    @classmethod
    def from_entity(cls, listener: ChatListener) -> "AddTelegramListenerResponseSchema":
        return cls(listener_id=listener.oid)


class ChatListenerListItemSchema(BaseModel):
    oid: str

    @classmethod
    def from_entity(cls, chat_listener: ChatListener) -> "ChatListenerListItemSchema":
        return cls(
            oid=chat_listener.oid,
        )
