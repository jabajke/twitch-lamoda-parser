import asyncio
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from src.core.settings import settings


class KafkaSetup:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.consumer = AIOKafkaConsumer(
            bootstrap_servers=settings.kafka_settings.KAFKA_BOOTSTRAP_SERVER,
            loop=self.loop
        )
        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.kafka_settings.KAFKA_BOOTSTRAP_SERVER,
            loop=self.loop
        )
