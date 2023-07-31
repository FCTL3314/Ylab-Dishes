from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.services import AbstractCRUDService
from app.menu.repository import MenuRepository
from app.menu.services import MENU_NOT_FOUND_MESSAGE
from app.models import Submenu
from app.utils import is_obj_exists_or_404

SUBMENU_NOT_FOUND_MESSAGE = "submenu not found"


class SubmenuService(AbstractCRUDService):
    async def retrieve(self, menu_id: UUID, submenu_id: UUID, session: AsyncSession):
        submenu = await self.repository.get(menu_id, submenu_id, session)
        is_obj_exists_or_404(submenu, SUBMENU_NOT_FOUND_MESSAGE)
        return submenu

    async def list(self, menu_id: UUID, session: AsyncSession):
        return await self.repository.all(menu_id, session)

    async def create(self, menu_id: UUID, submenu: Submenu, session: AsyncSession):
        menu = await MenuRepository.get_by_id(menu_id, session, orm_object=True)
        is_obj_exists_or_404(menu, MENU_NOT_FOUND_MESSAGE)
        return await self.repository.create(menu, submenu, session)

    async def update(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        updated_submenu: Submenu,
        session: AsyncSession,
    ):
        submenu = await self.repository.get_by_id(
            menu_id, submenu_id, session, orm_object=True
        )
        is_obj_exists_or_404(submenu, SUBMENU_NOT_FOUND_MESSAGE)
        return await self.repository.update(submenu, updated_submenu, session)

    async def delete(self, menu_id: UUID, submenu_id: UUID, session: AsyncSession):
        submenu = await self.repository.get_by_id(
            menu_id, submenu_id, session, orm_object=True
        )
        is_obj_exists_or_404(submenu, SUBMENU_NOT_FOUND_MESSAGE)
        return await self.repository.delete(submenu, session)
