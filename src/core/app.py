from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from kafka import KafkaClient
from kafka.admin import KafkaAdminClient, NewTopic
from loguru import logger

from lamoda_app import router as lamoda_router
from src.core.settings import LoggerConfig, settings
from src.services import InsertIntoMongoService
from twitch_app import router as twitch_router

logger.configure(**LoggerConfig.config)

app = FastAPI()

app.include_router(twitch_router)
app.include_router(lamoda_router)


@app.on_event("startup")
async def create_topic_if_not_exists(
        kafka_cfg=settings.kafka_settings
) -> None:
    """
    partition = 0 is lamoda_partition
    partition = 1 is lamoda_parser_partition
    partition = 2 is streamers_partition
    partition = 3 is games_partition
    partition = 4 is streams_partition
    """

    bootstrap_servers = kafka_cfg.KAFKA_BOOTSTRAP_SERVERS
    client = KafkaClient(
        bootstrap_servers=bootstrap_servers,
        api_version=(3, 3, 1)
    )
    admin_client = KafkaAdminClient(
        bootstrap_servers=bootstrap_servers,
        api_version=(3, 3, 1)
    )

    future = client.cluster.request_update()
    client.poll(future=future)
    metadata = client.cluster

    if kafka_cfg.KAFKA_TOPIC not in metadata.topics():
        logger.info('Topic creation..')
        topic = NewTopic(name=kafka_cfg.KAFKA_TOPIC, num_partitions=5, replication_factor=1)
        admin_client.create_topics(new_topics=[topic], validate_only=False)
        logger.info('Topic "{0}" was successfully created'.format(kafka_cfg.KAFKA_TOPIC))


@app.on_event("startup")
@repeat_every(seconds=60 * 20)
def insert_into_mongo() -> None:
    """
    Insert into database every 20 minutes
    :return: None
    """
    InsertIntoMongoService.insert_into_mongo()
