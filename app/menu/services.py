from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.services import AbstractCRUDService
from app.models import Menu
from app.utils import is_obj_exists_or_404

MENU_NOT_FOUND_MESSAGE = "menu not found"


class MenuService(AbstractCRUDService):
    async def retrieve(self, menu_id: UUID, session: AsyncSession):
        menu = await self.repository.get(menu_id, session)
        is_obj_exists_or_404(menu, MENU_NOT_FOUND_MESSAGE)
        return menu

    async def list(self, session: AsyncSession):
        return await self.repository.all(session)

    async def create(self, menu: Menu, session: AsyncSession):
        return await self.repository.create(menu, session)

    async def update(self, menu_id: UUID, updated_menu: Menu, session: AsyncSession):
        menu = await self.repository.get_by_id(menu_id, session, orm_object=True)
        is_obj_exists_or_404(menu, MENU_NOT_FOUND_MESSAGE)
        return await self.repository.update(menu, updated_menu, session)

    async def delete(self, menu_id: UUID, session: AsyncSession):
        menu = await self.repository.get_by_id(menu_id, session, orm_object=True)
        is_obj_exists_or_404(menu, MENU_NOT_FOUND_MESSAGE)
        return await self.repository.delete(menu, session)
