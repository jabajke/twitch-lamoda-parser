from fastapi import APIRouter

from .api import router as api_router

router = APIRouter(prefix='/lamoda', tags=['lamoda'])
router.include_router(api_router)
