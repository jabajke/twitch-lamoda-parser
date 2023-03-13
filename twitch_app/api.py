from fastapi import APIRouter, Depends, status

from .services import TwitchService

router = APIRouter(prefix='/twitch-parser')


@router.get('/check', status_code=status.HTTP_200_OK)
async def check(twitch: TwitchService = Depends()):
    token = await twitch.auth()
    games = await twitch.get_games(token)
    streams, logins = await twitch.get_streams_logins(token)
    streamers = await twitch.get_users(token, logins)
    await twitch.insert_obj(
        games=games,
        streamers=streamers,
        streams=streams
    )
    return {"mes": "ok"}
