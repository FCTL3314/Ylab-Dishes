from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.schemas import DeletionResponse
from app.common.services import AbstractCRUDService
from app.menu.repository import MenuRepository
from app.menu.services import MENU_NOT_FOUND_MESSAGE, CachedMenuService
from app.models import Submenu
from app.redis import get_cached_data_or_set_new, redis
from app.submenu.constants import (
    SUBMENU_CACHE_TEMPLATE,
    SUBMENUS_CACHE_KEY,
    SUBMENUS_CACHE_TIME,
)
from app.submenu.schemas import SubmenuBase
from app.utils import is_obj_exists_or_404

SUBMENU_NOT_FOUND_MESSAGE = 'submenu not found'


SubmenuResponseType = TypeVar('SubmenuResponseType', bound=SubmenuBase)


class SubmenuService(AbstractCRUDService, Generic[SubmenuResponseType]):
    async def retrieve(
        self, menu_id: UUID, submenu_id: UUID, session: AsyncSession
    ) -> SubmenuResponseType:
        submenu = await self.repository.get(menu_id, submenu_id, session)
        is_obj_exists_or_404(submenu, SUBMENU_NOT_FOUND_MESSAGE)
        return submenu

    async def list(
        self, menu_id: UUID, session: AsyncSession
    ) -> list[SubmenuResponseType]:
        return await self.repository.all(menu_id, session)

    async def create(
        self, menu_id: UUID, submenu: Submenu, session: AsyncSession
    ) -> SubmenuResponseType:
        menu = await MenuRepository.get_by_id(menu_id, session, orm_object=True)
        is_obj_exists_or_404(menu, MENU_NOT_FOUND_MESSAGE)
        return await self.repository.create(menu, submenu, session)

    async def update(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        updated_submenu: Submenu,
        session: AsyncSession,
    ) -> SubmenuResponseType:
        submenu = await self.repository.get_by_id(
            menu_id, submenu_id, session, orm_object=True
        )
        is_obj_exists_or_404(submenu, SUBMENU_NOT_FOUND_MESSAGE)
        return await self.repository.update(submenu, updated_submenu, session)

    async def delete(
        self, menu_id: UUID, submenu_id: UUID, session: AsyncSession
    ) -> DeletionResponse:
        submenu = await self.repository.get_by_id(
            menu_id, submenu_id, session, orm_object=True
        )
        is_obj_exists_or_404(submenu, SUBMENU_NOT_FOUND_MESSAGE)
        await self.repository.delete(submenu, session)
        return DeletionResponse(**{'status': True, 'message': 'The submenu has been deleted'})


class CachedSubmenuService(SubmenuService[SubmenuResponseType]):
    async def retrieve(
        self, menu_id: UUID, submenu_id: UUID, session: AsyncSession
    ) -> SubmenuResponseType:
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
    ) -> list[SubmenuResponseType]:
        submenus = await get_cached_data_or_set_new(
            key=SUBMENUS_CACHE_KEY,
            callback=lambda: super(CachedSubmenuService, self).list(menu_id, session),
            expiration=SUBMENUS_CACHE_TIME,
        )
        return submenus

    async def create(
        self, menu_id: UUID, submenu: Submenu, session: AsyncSession
    ) -> SubmenuResponseType:
        _submenu = await super().create(
            menu_id, submenu, session
        )
        await CachedSubmenuService.clear_list_cache()
        await CachedMenuService.clear_cache(menu_id)
        return _submenu

    async def update(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        updated_submenu: Submenu,
        session: AsyncSession,
    ) -> SubmenuResponseType:
        _updated_submenu = await super().update(
            menu_id, submenu_id, updated_submenu, session
        )
        await CachedSubmenuService.clear_cache(submenu_id)
        return _updated_submenu

    async def delete(
        self, menu_id: UUID, submenu_id: UUID, session: AsyncSession
    ) -> DeletionResponse:
        response = await super().delete(
            menu_id, submenu_id, session
        )
        await CachedSubmenuService.clear_cache(submenu_id)
        await CachedMenuService.clear_cache(menu_id)
        return response

    @staticmethod
    async def clear_retrieve_cache(submenu_id: UUID) -> None:
        await redis.unlink(SUBMENU_CACHE_TEMPLATE.format(id=submenu_id))

    @staticmethod
    async def clear_list_cache() -> None:
        await redis.unlink(SUBMENUS_CACHE_KEY)

    @classmethod
    async def clear_cache(cls, submenu_id: UUID) -> None:
        await cls.clear_retrieve_cache(submenu_id)
        await cls.clear_list_cache()
