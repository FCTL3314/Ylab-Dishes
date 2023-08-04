from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.services import AbstractCRUDService
from app.dish.constants import DISH_CACHE_TEMPLATE, DISHES_CACHE_KEY, DISHES_CACHE_TIME
from app.menu.services import CachedMenuService
from app.models import Dish
from app.redis import get_cached_data_or_set_new, redis
from app.submenu.repository import SubmenuRepository
from app.submenu.services import SUBMENU_NOT_FOUND_MESSAGE, SubmenuService
from app.utils import is_obj_exists_or_404

DISH_NOT_FOUND_MESSAGE = "dish not found"


class DishService(AbstractCRUDService):
    async def retrieve(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: AsyncSession
    ) -> Dish:
        dish = await get_cached_data_or_set_new(
            DISH_CACHE_TEMPLATE.format(id=dish_id),
            lambda: self.repository.get(menu_id, submenu_id, dish_id, session),
            DISHES_CACHE_TIME,
        )
        is_obj_exists_or_404(dish, DISH_NOT_FOUND_MESSAGE)
        return dish

    async def list(
        self, menu_id: UUID, submenu_id: UUID, session: AsyncSession
    ) -> list[Dish]:
        dishes = await get_cached_data_or_set_new(
            DISHES_CACHE_KEY,
            lambda: self.repository.all(menu_id, submenu_id, session),
            DISHES_CACHE_TIME,
        )
        return dishes

    async def create(
        self, menu_id: UUID, submenu_id: UUID, dish: Dish, session: AsyncSession
    ) -> Dish:
        submenu = await SubmenuRepository.get_by_id(
            menu_id, submenu_id, session, orm_object=True
        )
        is_obj_exists_or_404(submenu, SUBMENU_NOT_FOUND_MESSAGE)
        DishService.clear_list_cache()
        return await self.repository.create(submenu, dish, session)

    async def update(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        updated_dish: Dish,
        session: AsyncSession,
    ) -> Dish:
        dish = await self.repository.get_by_id(
            menu_id, submenu_id, dish_id, session, orm_object=True
        )
        is_obj_exists_or_404(dish, DISH_NOT_FOUND_MESSAGE)
        DishService.clear_all_cache(dish_id)
        return await self.repository.update(dish, updated_dish, session)

    async def delete(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: AsyncSession
    ) -> dict:
        dish = await self.repository.get_by_id(
            menu_id, submenu_id, dish_id, session, orm_object=True
        )
        is_obj_exists_or_404(dish, DISH_NOT_FOUND_MESSAGE)
        DishService.clear_all_cache(dish_id)
        SubmenuService.clear_all_cache(submenu_id)
        CachedMenuService.clear_all_cache(menu_id)
        return await self.repository.delete(dish, session)

    @staticmethod
    def clear_retrieve_cache(dish_id):
        redis.delete(DISH_CACHE_TEMPLATE.format(id=dish_id))

    @staticmethod
    def clear_list_cache():
        redis.delete(DISHES_CACHE_KEY)

    @classmethod
    def clear_all_cache(cls, dish_id):
        cls.clear_retrieve_cache(dish_id)
        cls.clear_list_cache()
