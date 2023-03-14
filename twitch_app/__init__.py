from fastapi import APIRouter
from .api import router as api_router

router = APIRouter(prefix='/twitch', tags=['twitch'])

router.include_router(api_router)
