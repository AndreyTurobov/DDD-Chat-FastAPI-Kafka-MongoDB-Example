from dataclasses import dataclass, field

from aiokafka import AIOKafkaConsumer
from aiokafka.producer import AIOKafkaProducer

from infra.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    consumer: AIOKafkaConsumer
    consumer_map: dict[str, AIOKafkaConsumer] = field(
        default_factory=dict,
        kw_only=True,
    )

    async def send_message(self, key: bytes, topic: str, value: bytes):
        await self.producer.send(topic=topic, key=key, value=value)

    async def start_consuming(self, topic: str):
        self.consumer.subscribe(topics=[topic])

    async def consume(self):
        return await self.consumer.getone()

    async def stop_consuming(self, topic: str):
        self.consumer.unsubscribe()

    async def start(self):
        await self.producer.start()

    async def close(self):
        await self.producer.stop()
