from pydantic import BaseSettings


class Web(BaseSettings):
    HOST: str
    PORT: int
    RELOAD: bool

    class Config:
        env_file = '.env'


class DatabaseSettings(BaseSettings):
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str

    class Config:
        env_file = '.env'


class TwitchSettings(BaseSettings):
    CLIENT_ID: str
    CLIENT_SECRET_KEY: str

    class Config:
        env_file = '.env'


class KafkaSettings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC: str = "kafka"
    KAFKA_CONSUMER_GROUP: str = "group-id"

    class Config:
        env_file = '.env'


class General:
    web: Web = Web()
    db: DatabaseSettings = DatabaseSettings()
    twitch_settings: TwitchSettings = TwitchSettings()
    kafka_settings: KafkaSettings = KafkaSettings()


settings = General()
