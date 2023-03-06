import uvicorn
from src.core.settings import settings

if __name__ == '__main__':
    uvicorn.run(
        'src.core.app:app',
        host=settings.web.HOST,
        port=settings.web.PORT,
        reload=settings.web.RELOAD
    )
