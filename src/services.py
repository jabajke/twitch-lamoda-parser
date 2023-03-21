from kafka_app.setup import setup
from src.core.database import all_collections
from src.utils import add_created_at


class InsertIntoMongoService:
    _lamoda_parser = all_collections['lamoda_parser']
    _lamoda = all_collections['lamoda']
    _games = all_collections['games']
    _streams = all_collections['streams']
    _streamers = all_collections['streamers']

    consumer = setup.consumer

    @classmethod
    def insert_into_mongo(cls) -> None:
        for mes in cls.consumer:
            if mes.partition == 0:
                cls._lamoda.insert_many(add_created_at(mes.value))

            elif mes.partition == 1:
                if len(mes.value) == 1:
                    cls._lamoda_parser.insert_one(
                        add_created_at(
                            mes.value[0]
                        ))
                else:
                    cls._lamoda_parser.insert_many(
                        add_created_at(mes.value)
                    )
            elif mes.partition == 2:
                cls._streamers.insert_many(add_created_at(mes.value))
            elif mes.partition == 3:
                cls._games.insert_many(add_created_at(mes.value))
            elif mes.partition == 4:
                cls._streams.insert_many(add_created_at(mes.value))
