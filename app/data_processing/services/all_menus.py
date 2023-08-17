from sqlalchemy.ext.asyncio import AsyncSession

from app.common.services import AbstractListService
from app.data_processing.constants import ALL_MENUS_CACHE_KEY, ALL_MENUS_CACHE_TIME
from app.menu.dependencies import menu_nested_service
from app.menu.schemas import MenuNestedResponse
from app.redis import get_cached_data_or_set_new


class AllMenusService(AbstractListService):
    """
    Service for getting all menus with all nested submenus and dishes.
    """
    async def list(self, session: AsyncSession) -> list[MenuNestedResponse]:
        return await menu_nested_service().list(session, scalar=True)


class CachedAllMenusService(AllMenusService):

    async def list(self, session: AsyncSession) -> list[MenuNestedResponse]:
        return await get_cached_data_or_set_new(
            key=ALL_MENUS_CACHE_KEY,
            callback=lambda: super(CachedAllMenusService, self).list(session),
            expiration=ALL_MENUS_CACHE_TIME,
        )
