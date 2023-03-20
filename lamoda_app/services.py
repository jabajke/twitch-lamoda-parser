import pydantic
import requests
from bs4 import BeautifulSoup
from bson import ObjectId

from src.core.database import all_collections

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str


class LamodaAPIDataService:
    _url = "https://www.lamoda.ru/api/v1/recommendations/section?section={0}&limit={1}&gender={2}"
    _lamoda_collection = all_collections.get('lamoda')

    def get_all(self, url: str) -> dict:
        res = requests.get(url)
        return res.json()


class LamodaParserService:
    lamoda_parser = all_collections.get('lamoda_parser')

    def get_response(self, url: pydantic.HttpUrl) -> requests.models.Response:
        res = requests.get(url)
        return res

    def parser(self, body: requests.models.Response) -> list:
        soup = BeautifulSoup(body.content, 'html.parser')
        item = soup.select_one('div', class_='_root_1pgxk_2')
        category = item.select_one('h1', class_='_titleText_641wy_15 ui-catalog-search-head-title').text.strip()
        catalog = item.find('div', class_='grid__catalog')
        goods = catalog.find_all('div', class_='x-product-card-description__microdata-wrap')
        item_list = []
        for good in goods:
            title = good.find_next('div', class_='x-product-card-description__product-name').text
            brand = good.find_next('div', class_='x-product-card-description__brand-name').text
            price = good.previous.text.strip()
            data = {
                'title': title,
                'brand': brand,
                'category': category
            }
            if price != '':
                data.update({'price': float(price[:-3].replace(' ', ''))})
                item_list.append(data)
        return item_list


class LamodaOutputDataService:
    _lamoda_parser = all_collections.get('lamoda_parser')
    _lamoda = all_collections.get('lamoda')

    def output_parser_data(self, limit: int) -> list:
        data = list(self._lamoda_parser.find())
        return data[:limit]

    def output_api_data(self, limit: int) -> list:
        data = list(self._lamoda.find())
        return data[:limit]
