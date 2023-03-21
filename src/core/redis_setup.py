import json
from functools import wraps

import redis.asyncio as aioredis
from bson import json_util
from loguru import logger

from .settings import settings

redis_client = aioredis.Redis(
    host=settings.redis_settings.REDIS_HOST,
    port=settings.redis_settings.REDIS_PORT,
    db=settings.redis_settings.REDIS_DB
)


def cache(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        key = f'{func.__name__}:{args}:{kwargs}'
        result = await redis_client.get(key)
        if result is None:
            logger.warning('Im in cache')
            result = json.loads(json_util.dumps(await func(*args, **kwargs)))
            await redis_client.set(key, str(result), ex=60 * 5)
        else:
            logger.warning('ALREADY CACHED')
        return result

    return wrapper
