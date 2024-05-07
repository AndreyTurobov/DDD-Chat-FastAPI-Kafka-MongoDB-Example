from dataclasses import dataclass
from typing import ClassVar

from domain.events.messages import (
    NewChatCreatedEvent,
    NewMessageReceivedEvent,
)
from infra.message_brokers.converters import convert_event_to_broker_message
from logic.events.base import (
    EventHandler,
    IntegrationEvent,
)


@dataclass
class NewChatCreatedEventHandler(EventHandler[NewChatCreatedEvent, None]):
    async def handle(self, event: NewChatCreatedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=event.chat_oid.encode(),
        )


@dataclass
class NewMessageReceivedEventHandler(EventHandler[NewMessageReceivedEvent, None]):
    async def handle(self, event: NewMessageReceivedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=event.chat_oid.encode(),
        )


@dataclass
class NewMessageReceivedFromBrokerEvent(IntegrationEvent):
    event_title: ClassVar[str] = "New Message Received From Broker"

    message_text: str
    message_oid: str
    chat_oid: str


@dataclass
class NewMessageReceivedFromBrokerEventHandler(
    EventHandler[NewMessageReceivedFromBrokerEvent, None],
):
    async def handle(self, event: NewMessageReceivedFromBrokerEvent) -> None:
        await self.connection_manager.send_all(
            key=event.chat_oid,
            bytes_=convert_event_to_broker_message(event=event),
        )
