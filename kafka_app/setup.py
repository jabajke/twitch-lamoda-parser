import json

from kafka import KafkaConsumer, KafkaProducer

from src.core.settings import settings


class KafkaSetup:
    def __init__(self, kafka_cfg: settings.kafka_settings = settings.kafka_settings):
        self.consumer = KafkaConsumer(
            kafka_cfg.KAFKA_TOPIC,
            bootstrap_servers=kafka_cfg.KAFKA_BOOTSTRAP_SERVERS,
            group_id=kafka_cfg.KAFKA_CONSUMER_GROUP,
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            consumer_timeout_ms=5000
        )
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_cfg.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )


setup = KafkaSetup()
