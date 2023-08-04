from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.services import AbstractCRUDService
from app.menu.constants import MENU_CACHE_TEMPLATE, MENUS_CACHE_KEY, MENUS_CACHE_TIME
from app.menu.schemas import MenuResponse
from app.models import Menu
from app.redis import get_cached_data_or_set_new, redis
from app.utils import is_obj_exists_or_404

MENU_NOT_FOUND_MESSAGE = "menu not found"


class MenuService(AbstractCRUDService):
    async def retrieve(
        self, menu_id: UUID, session: AsyncSession
    ) -> MenuResponse | MenuResponse:
        menu = await self.repository.get(menu_id, session)
        is_obj_exists_or_404(menu, MENU_NOT_FOUND_MESSAGE)
        return menu

    async def list(self, session: AsyncSession) -> list[MenuResponse] | list[MenuResponse]:
        return await self.repository.all(session)

    async def create(self, menu: Menu, session: AsyncSession) -> MenuResponse | MenuResponse:
        return await self.repository.create(menu, session)

    async def update(
        self, menu_id: UUID, updated_menu: Menu, session: AsyncSession
    ) -> MenuResponse | MenuResponse:
        menu = await self.repository.get_by_id(menu_id, session, orm_object=True)
        is_obj_exists_or_404(menu, MENU_NOT_FOUND_MESSAGE)
        return await self.repository.update(menu, updated_menu, session)

    async def delete(self, menu_id: UUID, session: AsyncSession) -> dict:
        menu = await self.repository.get_by_id(menu_id, session, orm_object=True)
        is_obj_exists_or_404(menu, MENU_NOT_FOUND_MESSAGE)
        return await self.repository.delete(menu, session)


class CachedMenuService(MenuService):
    async def retrieve(
        self, menu_id: UUID, session: AsyncSession
    ) -> MenuResponse | MenuResponse:
        menu = await get_cached_data_or_set_new(
            key=MENU_CACHE_TEMPLATE.format(id=menu_id),
            callback=lambda: super(CachedMenuService, self).retrieve(menu_id, session),
            expiration=MENUS_CACHE_TIME,
        )
        return menu

    async def list(self, session: AsyncSession) -> list[MenuResponse] | list[MenuResponse]:
        menus = await get_cached_data_or_set_new(
            key=MENUS_CACHE_KEY,
            callback=lambda: super(CachedMenuService, self).list(session),
            expiration=MENUS_CACHE_TIME,
        )
        return menus

    async def create(self, menu: Menu, session: AsyncSession) -> MenuResponse | MenuResponse:
        menu = await super().create(menu, session)
        CachedMenuService.clear_list_cache()
        return menu

    async def update(
        self, menu_id: UUID, updated_menu: Menu, session: AsyncSession
    ) -> MenuResponse | MenuResponse:
        updated_menu = await super().update(menu_id, updated_menu, session)
        CachedMenuService.clear_all_cache(menu_id)
        return updated_menu

    async def delete(self, menu_id: UUID, session: AsyncSession) -> dict:
        response = await super().delete(menu_id, session)
        CachedMenuService.clear_all_cache(menu_id)
        return response

    @staticmethod
    def clear_retrieve_cache(menu_id: UUID) -> None:
        redis.delete(MENU_CACHE_TEMPLATE.format(id=menu_id))

    @staticmethod
    def clear_list_cache() -> None:
        redis.delete(MENUS_CACHE_KEY)

    @classmethod
    def clear_all_cache(cls, manu_id: UUID) -> None:
        cls.clear_retrieve_cache(manu_id)
        cls.clear_list_cache()
