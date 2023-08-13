import pickle
from typing import Any, Callable

import aioredis

from app.config import Config

redis = aioredis.from_url(Config.REDIS_URL)


async def get_cached_data_or_set_new(
    key: str, callback: Callable, expiration: int
) -> Any:
    """
    Returns the cached data if it exists, otherwise calls the
    callback function to get and cache the data.
    """
    cached_data = await redis.get(key)
    if cached_data is not None:
        return pickle.loads(cached_data)
    new_data = await callback()
    await redis.set(key, pickle.dumps(new_data), ex=expiration)
    return new_data
