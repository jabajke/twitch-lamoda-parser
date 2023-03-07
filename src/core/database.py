from pymongo import mongo_client

from .settings import settings

client = mongo_client.MongoClient(settings.db.DATABASE_URL)
db = client[settings.db.MONGO_INITDB_DATABASE]
lamoda_collection = db['lamoda']
