from uuid import UUID

from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.repository import BaseCRUDRepository
from app.menu.repository import MenuRepository
from app.models import Dish, Menu, Submenu
from app.utils import get_first_or_404

SUBMENU_NOT_FOUND_MESSAGE = "submenu not found"


class SubmenuRepository(BaseCRUDRepository):
    @staticmethod
    def get_base_query(menu_id: UUID):
        return select(Submenu).where(Submenu.menu_id == menu_id)

    @staticmethod
    async def get_by_id(
        menu_id: UUID, submenu_id: UUID, session: AsyncSession, orm_object: bool = False
    ):
        result = await get_first_or_404(
            SubmenuRepository.get_base_query(menu_id).where(Submenu.id == submenu_id),
            session,
            SUBMENU_NOT_FOUND_MESSAGE,
        )
        return result[0] if orm_object else result

    async def retrieve(self, menu_id: UUID, submenu_id: UUID, session: AsyncSession):
        query = self.get_base_query(menu_id).where(
            Submenu.id == submenu_id,
        )
        return await get_first_or_404(
            query,
            session,
            SUBMENU_NOT_FOUND_MESSAGE,
        )

    async def list(self, menu_id: UUID, session: AsyncSession):
        result = await session.execute(self.get_base_query(menu_id))
        return result.all()

    async def create(self, menu_id: UUID, submenu: Submenu, session: AsyncSession):
        menu = await MenuRepository.get_by_id(menu_id, session, orm_object=True)
        menu.submenus.append(submenu)
        session.add(submenu)
        await session.commit()
        await session.refresh(submenu)
        return await self.retrieve(menu_id, submenu.id, session)

    async def update(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        updated_submenu: Submenu,
        session: AsyncSession,
    ):
        submenu = await self.get_by_id(menu_id, submenu_id, session, orm_object=True)

        updated_submenu_dict = updated_submenu.dict(exclude_unset=True)
        for key, val in updated_submenu_dict.items():
            setattr(submenu, key, val)

        await session.commit()
        await session.refresh(submenu)
        return await self.retrieve(menu_id, submenu.id, session)

    async def delete(self, menu_id: UUID, submenu_id: UUID, session: AsyncSession):
        submenu = await self.get_by_id(menu_id, submenu_id, session, orm_object=True)
        await session.delete(submenu)
        await session.commit()
        return {"status": True, "message": "The submenu has been deleted"}


class SubmenuWithCountingRepository(SubmenuRepository):
    def get_base_query(self, menu_id: UUID):
        return (
            select(
                Submenu.id,
                Submenu.title,
                Submenu.description,
                func.count(distinct(Dish.id)).label("dishes_count"),
            )
            .outerjoin(Menu, Submenu.menu_id == Menu.id)
            .outerjoin(Dish, Dish.submenu_id == Submenu.id)
            .where(Menu.id == menu_id)
            .group_by(Submenu.id)
        )
