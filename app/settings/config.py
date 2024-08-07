from pydantic.fields import Field
from pydantic_settings.main import BaseSettings


class Config(BaseSettings):
    mongodb_connection_uri: str = Field(default="uri", alias="MONGO_DB_CONNECTION_URI")
    mongodb_chat_database: str = Field(default="chat", alias="MONGO_DB_CHAT_DATABASE")
    mongodb_chat_collection: str = Field(
        default="chat",
        alias="MONGO_DB_CHAT_COLLECTION",
    )
    mongodb_messages_collection: str = Field(
        default="messages",
        alias="MONGO_DB_MESSAGES_COLLECTION",
    )

    new_message_received_topic: str = Field(default="new-messages")
    new_chats_event_topic: str = Field(default="new-chats-topic")
    chat_deleted_event_topic: str = Field(default="chat-deleted")
    new_listener_added_topic: str = Field(default="new-listener-added")

    kafka_url: str = Field(alias="KAFKA_URL")
