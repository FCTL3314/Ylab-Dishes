from uuid import UUID

from app.menu.constants import MENU_CACHE_TEMPLATE, MENUS_CACHE_KEY
from app.redis import redis


async def clear_menu_retrieve_cache(menu_id: UUID) -> None:
    await redis.unlink(MENU_CACHE_TEMPLATE.format(id=menu_id))


async def clear_menu_list_cache() -> None:
    await redis.unlink(MENUS_CACHE_KEY)


async def clear_menu_cache(menu_id: UUID) -> None:
    await clear_menu_retrieve_cache(menu_id)
    await clear_menu_list_cache()
