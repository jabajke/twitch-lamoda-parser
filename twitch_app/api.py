from fastapi import APIRouter, Depends, status

from .schemas import OutputDataTwitchSchema
from .services import TwitchOutputDataService, TwitchService

router = APIRouter(prefix='/twitch-parser')


@router.get('/api-scrapper', status_code=status.HTTP_200_OK)
async def api_scrapper(twitch: TwitchService = Depends()):
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


@router.post(
    '/twitch-output',
    status_code=status.HTTP_200_OK
)
async def twitch_output(
        schema: OutputDataTwitchSchema,
        twitch: TwitchOutputDataService = Depends(),
        limit: int = 10
):
    data = twitch.choose_output(schema.dict(), limit)
    return data
