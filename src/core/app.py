from fastapi import FastAPI

from lamoda_app import router as lamoda_router
from twitch_app import router as twitch_router

app = FastAPI()

app.include_router(twitch_router)
app.include_router(lamoda_router)
