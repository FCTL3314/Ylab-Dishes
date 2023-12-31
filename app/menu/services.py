from typing import Generic, TypeVar
from uuid import UUID

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.schemas import DeletionResponse
from app.common.services import AbstractCRUDService
from app.menu.cache import clear_menu_cache, clear_menu_list_cache
from app.menu.constants import MENU_CACHE_TEMPLATE, MENUS_CACHE_KEY, MENUS_CACHE_TIME
from app.menu.schemas import MenuBase
from app.models import Menu
from app.redis import get_cached_data_or_set_new
from app.utils import is_obj_exists_or_404

MENU_NOT_FOUND_MESSAGE = 'menu not found'


MenuResponseType = TypeVar('MenuResponseType', bound=MenuBase)


class MenuService(AbstractCRUDService, Generic[MenuResponseType]):
    async def retrieve(
        self, menu_id: UUID, session: AsyncSession
    ) -> MenuResponseType:
        menu = await self.repository.get(menu_id, session)
        is_obj_exists_or_404(menu, MENU_NOT_FOUND_MESSAGE)
        return menu

    async def list(
        self, session: AsyncSession, scalar: bool = False
    ) -> list[MenuResponseType]:
        return await self.repository.all(session, scalar)

    async def create(
        self, menu: Menu, background_tasks: BackgroundTasks, session: AsyncSession
    ) -> MenuResponseType:
        return await self.repository.create(menu, session)

    async def update(
        self, menu_id: UUID, updated_menu: Menu, background_tasks: BackgroundTasks, session: AsyncSession
    ) -> MenuResponseType:
        menu = await self.repository.get_by_id(menu_id, session, orm_object=True)
        is_obj_exists_or_404(menu, MENU_NOT_FOUND_MESSAGE)
        return await self.repository.update(menu, updated_menu, session)

    async def delete(self, menu_id: UUID, background_tasks: BackgroundTasks, session: AsyncSession) -> DeletionResponse:
        menu = await self.repository.get_by_id(menu_id, session, orm_object=True)
        is_obj_exists_or_404(menu, MENU_NOT_FOUND_MESSAGE)
        await self.repository.delete(menu, session)
        return DeletionResponse(status=True, message='The menu has been deleted')


class CachedMenuService(MenuService[MenuResponseType]):
    async def retrieve(
        self, menu_id: UUID, session: AsyncSession
    ) -> MenuResponseType:
        menu = await get_cached_data_or_set_new(
            key=MENU_CACHE_TEMPLATE.format(id=menu_id),
            callback=lambda: super(CachedMenuService, self).retrieve(menu_id, session),
            expiration=MENUS_CACHE_TIME,
        )
        return menu

    async def list(
        self, session: AsyncSession, scalar: bool = False
    ) -> list[MenuResponseType]:
        menus = await get_cached_data_or_set_new(
            key=MENUS_CACHE_KEY,
            callback=lambda: super(CachedMenuService, self).list(session, scalar),
            expiration=MENUS_CACHE_TIME,
        )
        return menus

    async def create(
        self, menu: Menu, background_tasks: BackgroundTasks, session: AsyncSession
    ) -> MenuResponseType:
        _menu = await super().create(menu, background_tasks, session)
        background_tasks.add_task(clear_menu_list_cache)
        return _menu

    async def update(
        self, menu_id: UUID, updated_menu: Menu, background_tasks: BackgroundTasks, session: AsyncSession
    ) -> MenuResponseType:
        _updated_menu = await super().update(menu_id, updated_menu, background_tasks, session)
        background_tasks.add_task(clear_menu_cache, menu_id)
        return _updated_menu

    async def delete(self, menu_id: UUID, background_tasks: BackgroundTasks, session: AsyncSession) -> DeletionResponse:
        response = await super().delete(menu_id, background_tasks, session)
        background_tasks.add_task(clear_menu_cache, menu_id)
        return response
