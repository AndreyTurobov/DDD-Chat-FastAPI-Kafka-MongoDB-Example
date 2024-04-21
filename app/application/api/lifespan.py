import asyncio

import aiokafka

from infra.message_brokers.base import BaseMessageBroker
from logic.init import init_container


async def init_message_broker():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.start()

# async def start_kafka(retry_interval=1, max_retries=3):
#     retries = 0
#     container = init_container()
#     message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
#     while retries < max_retries:
#         try:
#             await message_broker.producer.start()
#             print("Kafka connection established successfully.")
#             return
#         except aiokafka.errors.KafkaConnectionError:
#             print(f"Failed to connect to Kafka. Retrying in {retry_interval} seconds...")
#             await asyncio.sleep(retry_interval)
#             retries += 1
#             retry_interval *= 2  # Exponential backoff
#     print("Max retries reached. Failed to establish connection to Kafka.")

async def close_message_broker():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.close()
