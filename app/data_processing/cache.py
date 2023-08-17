from app.data_processing.constants import ALL_MENUS_CACHE_KEY
from app.redis import redis


async def clear_menus_with_nested_objects_cache():
    await redis.unlink(ALL_MENUS_CACHE_KEY)
