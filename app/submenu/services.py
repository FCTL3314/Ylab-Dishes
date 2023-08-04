from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.services import AbstractCRUDService
from app.menu.repository import MenuRepository
from app.menu.services import MENU_NOT_FOUND_MESSAGE, CachedMenuService
from app.models import Submenu
from app.redis import get_cached_data_or_set_new, redis
from app.submenu.constants import (SUBMENU_CACHE_TEMPLATE, SUBMENUS_CACHE_KEY,
                                   SUBMENUS_CACHE_TIME)
from app.submenu.schemas import SubmenuResponse
from app.utils import is_obj_exists_or_404

SUBMENU_NOT_FOUND_MESSAGE = "submenu not found"


class SubmenuService(AbstractCRUDService):
    async def retrieve(
        self, menu_id: UUID, submenu_id: UUID, session: AsyncSession
    ) -> Submenu | SubmenuResponse:
        submenu = await self.repository.get(menu_id, submenu_id, session)
        is_obj_exists_or_404(submenu, SUBMENU_NOT_FOUND_MESSAGE)
        return submenu

    async def list(
        self, menu_id: UUID, session: AsyncSession
    ) -> list[Submenu] | list[SubmenuResponse]:
        return await self.repository.all(menu_id, session)

    async def create(
        self, menu_id: UUID, submenu: Submenu, session: AsyncSession
    ) -> Submenu | SubmenuResponse:
        menu = await MenuRepository.get_by_id(menu_id, session, orm_object=True)
        is_obj_exists_or_404(menu, MENU_NOT_FOUND_MESSAGE)
        return await self.repository.create(menu, submenu, session)

    async def update(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        updated_submenu: Submenu,
        session: AsyncSession,
    ) -> Submenu | SubmenuResponse:
        submenu = await self.repository.get_by_id(
            menu_id, submenu_id, session, orm_object=True
        )
        is_obj_exists_or_404(submenu, SUBMENU_NOT_FOUND_MESSAGE)
        return await self.repository.update(submenu, updated_submenu, session)

    async def delete(
        self, menu_id: UUID, submenu_id: UUID, session: AsyncSession
    ) -> dict:
        submenu = await self.repository.get_by_id(
            menu_id, submenu_id, session, orm_object=True
        )
        is_obj_exists_or_404(submenu, SUBMENU_NOT_FOUND_MESSAGE)
        return await self.repository.delete(submenu, session)


class CachedSubmenuService(SubmenuService):
    async def retrieve(
        self, menu_id: UUID, submenu_id: UUID, session: AsyncSession
    ) -> Submenu | SubmenuResponse:
        submenu = await get_cached_data_or_set_new(
            key=SUBMENU_CACHE_TEMPLATE.format(id=submenu_id),
            callback=lambda: super(CachedSubmenuService, self).retrieve(
                menu_id, submenu_id, session
            ),
            expiration=SUBMENUS_CACHE_TIME,
        )
        return submenu

    async def list(
        self, menu_id: UUID, session: AsyncSession
    ) -> list[Submenu] | list[SubmenuResponse]:
        submenus = await get_cached_data_or_set_new(
            key=SUBMENUS_CACHE_KEY,
            callback=lambda: super(CachedSubmenuService, self).list(menu_id, session),
            expiration=SUBMENUS_CACHE_TIME,
        )
        return submenus

    async def create(
        self, menu_id: UUID, submenu: Submenu, session: AsyncSession
    ) -> Submenu | SubmenuResponse:
        submenu = await super(CachedSubmenuService, self).create(
            menu_id, submenu, session
        )
        CachedSubmenuService.clear_list_cache()
        CachedMenuService.clear_all_cache(menu_id)
        return submenu

    async def update(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        updated_submenu: Submenu,
        session: AsyncSession,
    ) -> Submenu | SubmenuResponse:
        updated_submenu = await super(CachedSubmenuService, self).update(
            menu_id, submenu_id, updated_submenu, session
        )
        CachedSubmenuService.clear_all_cache(submenu_id)
        return updated_submenu

    async def delete(
        self, menu_id: UUID, submenu_id: UUID, session: AsyncSession
    ) -> dict:
        response = await super(CachedSubmenuService, self).delete(
            menu_id, submenu_id, session
        )
        CachedSubmenuService.clear_all_cache(submenu_id)
        CachedMenuService.clear_all_cache(menu_id)
        return response

    @staticmethod
    def clear_retrieve_cache(submenu_id):
        redis.delete(SUBMENU_CACHE_TEMPLATE.format(id=submenu_id))

    @staticmethod
    def clear_list_cache():
        redis.delete(SUBMENUS_CACHE_KEY)

    @classmethod
    def clear_all_cache(cls, submenu_id):
        cls.clear_retrieve_cache(submenu_id)
        cls.clear_list_cache()
