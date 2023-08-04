import pickle
from typing import Any, Callable

import redis

from app.config import Config

redis = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0)


async def get_cached_data_or_set_new(
    key: str, callback: Callable, expiration: int
) -> Any:
    cached_data = redis.get(key)
    if cached_data is not None:
        return pickle.loads(cached_data)
    new_data = await callback()
    redis.set(key, pickle.dumps(new_data), ex=expiration)
    return new_data
