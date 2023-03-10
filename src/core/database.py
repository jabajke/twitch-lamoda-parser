from pymongo import errors, mongo_client

from lamoda_app.mongo_schemas import lamoda_item_schema

from .settings import settings

client = mongo_client.MongoClient(settings.db.DATABASE_URL)
db = client[settings.db.MONGO_INITDB_DATABASE]


def collections():
    try:
        db.validate_collection('lamoda')
    except errors.OperationFailure:
        db.create_collection('lamoda')

    try:
        db.validate_collection('lamoda_parser')
    except errors.OperationFailure:
        db.create_collection(
            'lamoda_parser',
            validator=lamoda_item_schema,
            validationLevel='moderate'
        )

    return {
        'lamoda': db['lamoda'],
        'lamoda_parser': db['lamoda_parser']
    }


all_collections = collections()
