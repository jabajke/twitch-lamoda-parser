from pymongo import errors, mongo_client

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

    return {
        'streams': db['streams'],
        'games': db['games'],
        'streamers': db['streamers']
    }


all_collections = collections()
