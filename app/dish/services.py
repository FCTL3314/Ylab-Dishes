from typing import Generic, TypeVar
from uuid import UUID

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.schemas import DeletionResponse
from app.common.services import AbstractCRUDService
from app.dish.constants import DISH_CACHE_TEMPLATE, DISHES_CACHE_KEY, DISHES_CACHE_TIME
from app.dish.schemas import DishBase
from app.menu.services import CachedMenuService
from app.models import Dish
from app.redis import get_cached_data_or_set_new, redis
from app.submenu.repository import SubmenuRepository
from app.submenu.services import SUBMENU_NOT_FOUND_MESSAGE, CachedSubmenuService
from app.utils import is_obj_exists_or_404

DISH_NOT_FOUND_MESSAGE = 'dish not found'

DishResponseType = TypeVar('DishResponseType', bound=DishBase)


class DishService(AbstractCRUDService, Generic[DishResponseType]):
    async def retrieve(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: AsyncSession, scalar: bool = False
    ) -> DishResponseType:
        dish = await self.repository.get(menu_id, submenu_id, dish_id, session, scalar)
        is_obj_exists_or_404(dish, DISH_NOT_FOUND_MESSAGE)
        return dish

    async def list(
        self, menu_id: UUID, submenu_id: UUID, session: AsyncSession, scalar: bool = False
    ) -> list[DishResponseType]:
        return await self.repository.all(menu_id, submenu_id, session, scalar)

    async def create(
        self, menu_id: UUID, submenu_id: UUID, dish: Dish, background_tasks: BackgroundTasks, session: AsyncSession
    ) -> DishResponseType:
        submenu = await SubmenuRepository.get_by_id(
            menu_id, submenu_id, session, orm_object=True
        )
        is_obj_exists_or_404(submenu, SUBMENU_NOT_FOUND_MESSAGE)
        return await self.repository.create(submenu.id, dish, session)  # type: ignore

    async def update(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        updated_dish: Dish,
        background_tasks: BackgroundTasks,
        session: AsyncSession,
    ) -> DishResponseType:
        dish = await self.repository.get_by_id(
            menu_id, submenu_id, dish_id, session, orm_object=True
        )
        is_obj_exists_or_404(dish, DISH_NOT_FOUND_MESSAGE)
        return await self.repository.update(dish, updated_dish, session)

    async def delete(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, background_tasks: BackgroundTasks, session: AsyncSession
    ) -> DeletionResponse:
        dish = await self.repository.get_by_id(
            menu_id, submenu_id, dish_id, session, orm_object=True
        )
        is_obj_exists_or_404(dish, DISH_NOT_FOUND_MESSAGE)
        await self.repository.delete(dish, session)
        return DeletionResponse(status=True, message='The dish has been deleted')


class CachedDishService(DishService[DishResponseType]):
    async def retrieve(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: AsyncSession, scalar: bool = False
    ) -> DishResponseType:
        dish = await get_cached_data_or_set_new(
            DISH_CACHE_TEMPLATE.format(id=dish_id),
            lambda: super(CachedDishService, self).retrieve(
                menu_id, submenu_id, dish_id, session, scalar
            ),
            DISHES_CACHE_TIME,
        )
        is_obj_exists_or_404(dish, DISH_NOT_FOUND_MESSAGE)
        return dish

    async def list(
        self, menu_id: UUID, submenu_id: UUID, session: AsyncSession, scalar: bool = False
    ) -> list[DishResponseType]:
        dishes = await get_cached_data_or_set_new(
            DISHES_CACHE_KEY,
            lambda: super(CachedDishService, self).list(menu_id, submenu_id, session, scalar),
            DISHES_CACHE_TIME,
        )
        return dishes

    async def create(
        self, menu_id: UUID, submenu_id: UUID, dish: Dish, background_tasks: BackgroundTasks, session: AsyncSession
    ) -> DishResponseType:
        submenu = await super().create(menu_id, submenu_id, dish, background_tasks, session)
        background_tasks.add_task(CachedDishService.clear_list_cache)
        background_tasks.add_task(CachedSubmenuService.clear_list_cache)
        background_tasks.add_task(CachedMenuService.clear_list_cache)
        return submenu

    async def update(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        updated_dish: Dish,
        background_tasks: BackgroundTasks,
        session: AsyncSession,
    ) -> DishResponseType:
        dish = await super().update(menu_id, submenu_id, dish_id, updated_dish, background_tasks, session)
        background_tasks.add_task(CachedDishService.clear_cache, dish_id)
        return dish

    async def delete(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, background_tasks: BackgroundTasks, session: AsyncSession
    ) -> DeletionResponse:
        response = await super().delete(menu_id, submenu_id, dish_id, background_tasks, session)
        background_tasks.add_task(CachedDishService.clear_cache, dish_id)
        background_tasks.add_task(CachedSubmenuService.clear_cache, submenu_id)
        background_tasks.add_task(CachedMenuService.clear_cache, menu_id)
        return response

    @staticmethod
    async def clear_retrieve_cache(dish_id):
        await redis.unlink(DISH_CACHE_TEMPLATE.format(id=dish_id))

    @staticmethod
    async def clear_list_cache():
        await redis.unlink(DISHES_CACHE_KEY)

    @classmethod
    async def clear_cache(cls, dish_id):
        await cls.clear_retrieve_cache(dish_id)
        await cls.clear_list_cache()
