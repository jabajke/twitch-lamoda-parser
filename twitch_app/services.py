import requests

from src.core.database import all_collections
from src.core.settings import settings


class TwitchService:

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


class TwitchOutputDataService:
    _games = all_collections['games']
    _streams = all_collections['streams']
    _streamers = all_collections['streamers']

    def output_games(self, limit):
        data = list(self._games.find())
        return data[:limit]

    def output_streams(self, limit):
        data = list(self._streams.find())
        return data[:limit]

    def output_streamers(self, limit):
        data = list(self._streamers.find())
        return data[:limit]

    def choose_output(self, data, limit):
        if data.get('types') == 'games':
            return self.output_games(limit)
        elif data.get('types') == 'streams':
            return self.output_streams(limit)
        else:
            return self.output_streamers(limit)
