import pydantic
import requests
from bson import ObjectId

from src.core.database import lamoda_collection

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str


class LamodaAPIDataService:
    url = "https://www.lamoda.ru/api/v1/recommendations/section?section={0}&limit={1}&gender={2}"

    @classmethod
    def get_all(cls, url):
        res = requests.get(url)
        return res.json()

    @classmethod
    def create_lamoda_item(cls, data):
        if data is None:
            lamoda_collection.insert_one(data)
        else:
            lamoda_collection.insert_many(data)