import requests


class LamodaAPIDataService:

    @classmethod
    def get_all(cls, url):
        res = requests.get(url)
        return res.json()
