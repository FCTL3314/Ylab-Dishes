from uuid import UUID

from app.dish.constants import DISH_CACHE_TEMPLATE, DISHES_CACHE_TEMPLATE
from app.redis import redis


async def clear_dish_retrieve_cache(dish_id: UUID):
    await redis.unlink(DISH_CACHE_TEMPLATE.format(id=dish_id))


async def clear_dish_list_cache(menu_id: UUID, submenu_id: UUID):
    await redis.unlink(DISHES_CACHE_TEMPLATE.format(menu_id=menu_id, submenu_id=submenu_id))


async def clear_dish_cache(menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    await clear_dish_retrieve_cache(dish_id)
    await clear_dish_list_cache(menu_id, submenu_id)
