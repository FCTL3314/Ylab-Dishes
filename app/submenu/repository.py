from uuid import UUID

from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.repository import AbstractCRUDRepository
from app.models import Dish, Menu, Submenu


class SubmenuRepository(AbstractCRUDRepository):
    @staticmethod
    def get_base_query(menu_id: UUID):
        return select(Submenu).where(Submenu.menu_id == menu_id)

    @staticmethod
    async def get_by_id(
        menu_id: UUID, submenu_id: UUID, session: AsyncSession, orm_object: bool = False
    ):
        stmt = SubmenuRepository.get_base_query(menu_id).where(Submenu.id == submenu_id)
        result = await session.execute(stmt)
        return result.first()[0] if orm_object else result.first()

    async def retrieve(self, menu_id: UUID, submenu_id: UUID, session: AsyncSession):
        stmt = self.get_base_query(menu_id).where(
            Submenu.id == submenu_id,
        )
        result = await session.execute(stmt)
        return result.first()

    async def list(self, menu_id: UUID, session: AsyncSession):
        result = await session.execute(self.get_base_query(menu_id))
        return result.all()

    async def create(self, menu: Menu, submenu: Submenu, session: AsyncSession):
        menu.submenus.append(submenu)
        session.add(submenu)
        await session.commit()
        await session.refresh(submenu)
        return await self.retrieve(submenu.menu_id, submenu.id, session)

    async def update(
        self,
        submenu: Submenu,
        updated_submenu: Submenu,
        session: AsyncSession,
    ):
        updated_submenu_dict = updated_submenu.dict(exclude_unset=True)
        for key, val in updated_submenu_dict.items():
            setattr(submenu, key, val)

        await session.commit()
        await session.refresh(submenu)
        return await self.retrieve(submenu.menu_id, submenu.id, session)

    async def delete(self, submenu: Submenu, session: AsyncSession):
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
