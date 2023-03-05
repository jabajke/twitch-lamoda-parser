from pydantic import BaseSettings


class Web(BaseSettings):
    host: str
    port: int
    reload: bool = True

    class Config:
        env_file = '.env'


web = Web()
