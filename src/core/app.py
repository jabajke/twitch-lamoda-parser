from fastapi import FastAPI

from lamoda_app import router

app = FastAPI()

app.include_router(router)
