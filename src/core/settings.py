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


class General:
    web: Web = Web()
    db: DatabaseSettings = DatabaseSettings()


settings = General()
