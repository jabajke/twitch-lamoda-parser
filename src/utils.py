from datetime import datetime
from typing import Union

from kafka_app.setup import setup
from src.core.settings import settings


def add_created_at(var):
    if isinstance(var, list):
        var = [dict(item, created_at=datetime.utcnow()) for item in var]
    else:
        var.update(dict(created_at=datetime.utcnow()))
    return var


def send_to_kafka(
        goods: Union[list, dict],
        partition: int,
        producer=setup.producer
) -> None:
    producer.send(
        topic=settings.kafka_settings.KAFKA_TOPIC,
        value=goods,
        partition=partition
    )
