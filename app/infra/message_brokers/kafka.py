from collections.abc import AsyncIterator
from dataclasses import dataclass

from aiokafka.consumer.consumer import AIOKafkaConsumer
from aiokafka.producer.producer import AIOKafkaProducer
import orjson

from infra.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    consumer: AIOKafkaConsumer

    async def send_message(self, key: bytes, topic: str, value: bytes) -> None:
        await self.producer.send(topic=topic, key=key, value=value)

    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        self.consumer.subscribe(topics=[topic])

        async for message in self.consumer:
            yield orjson.loads(message.value)

    async def stop_consuming(self, topic: str) -> None:
        self.consumer.unsubscribe()

    async def close(self) -> None:
        await self.consumer.stop()
        await self.producer.stop()

    async def start(self) -> None:
        await self.producer.start()
        await self.consumer.start()
