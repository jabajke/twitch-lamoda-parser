import uvicorn
from src.core.settings import web

if __name__ == '__main__':
    uvicorn.run(
        'src.core.app:app',
        host=web.host,
        port=web.port,
        reload=web.reload
    )
