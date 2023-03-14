import requests

from src.core.database import all_collections
from src.core.settings import settings
from src.utils import add_created_at

from .enums import TwitchTypes


class TwitchService:
    _games = all_collections.get('games')
    _streams = all_collections.get('streams')
    _streamers = all_collections.get('streamers')
    _obj_type: TwitchTypes = TwitchTypes

    async def auth(self):
        data = {
            'client_id': settings.twitch_settings.CLIENT_ID,
            'client_secret': settings.twitch_settings.CLIENT_SECRET_KEY,
            'grant_type': 'client_credentials'
        }
        url = 'https://id.twitch.tv/oauth2/token'
        res = requests.post(url, data)
        return res.json()['access_token']

    async def get_games(self, token) -> dict:
        url = 'https://api.twitch.tv/helix/games/top'
        res = requests.get(url, headers={
            'Authorization': f'Bearer {token}',
            'Client-Id': settings.twitch_settings.CLIENT_ID
        })
        games = res.json()['data']
        return games

    async def get_streams_logins(self, token) -> tuple:
        url = 'https://api.twitch.tv/helix/streams?first=100'
        res = requests.get(url, headers={
            'Authorization': f'Bearer {token}',
            'Client-Id': settings.twitch_settings.CLIENT_ID
        })
        streams = res.json()['data']
        user_logins = ''
        for stream in streams:
            user_logins += stream.get('user_login') + '&' 'login='
        return streams, user_logins

    async def get_users(self, token, user_logins: str) -> dict:
        user_logins = user_logins[:-7]
        url = 'https://api.twitch.tv/helix/users?login={}'.format(user_logins)
        res = requests.get(url, headers={
            'Authorization': f'Bearer {token}',
            'Client-Id': settings.twitch_settings.CLIENT_ID
        })
        streamers = res.json()['data']
        return streamers

    async def insert_obj(self, games, streamers, streams) -> None:
        self._games.insert_many(add_created_at(games))
        self._streams.insert_many(add_created_at(streams))
        self._streamers.insert_many(add_created_at(streamers))
