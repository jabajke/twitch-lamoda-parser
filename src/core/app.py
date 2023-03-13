from fastapi import FastAPI

from twitch_app import router as twitch_router

app = FastAPI()

app.include_router(twitch_router)
