from pymongo import errors, mongo_client

from lamoda_app.mongo_schemas import lamoda_item_schema

from .settings import settings

client = mongo_client.MongoClient(host=settings.db.DATABASE_URL)

db = client[settings.db.MONGO_INITDB_DATABASE]


def collections():
    try:
        db.validate_collection('streams')
    except errors.OperationFailure:
        db.create_collection('streams')

    try:
        db.validate_collection('games')
    except errors.OperationFailure:
        db.create_collection('games')

    try:
        db.validate_collection('streamers')
    except errors.OperationFailure:
        db.create_collection('streamers')
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
        'streams': db['streams'],
        'games': db['games'],
        'streamers': db['streamers'],
        'lamoda': db['lamoda'],
        'lamoda_parser': db['lamoda_parser']
    }


all_collections = collections()
