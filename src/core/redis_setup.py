import json
from ast import literal_eval
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
            logger.info('Cache Hit')
            result = json.loads(json_util.dumps(await func(*args, **kwargs)))
            await redis_client.set(key, str(result), ex=60 * 5)
        else:
            logger.info('Already Cached')
        return result if isinstance(result, list) else json.loads(
            json.dumps(
                literal_eval(result.decode('utf-8'))
            ))

    return wrapper
