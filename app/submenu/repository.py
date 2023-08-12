from uuid import UUID

from sqlalchemy import distinct, func, select
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from app.common.repository import AbstractCRUDRepository
from app.models import Dish, Menu, Submenu


class SubmenuRepository(AbstractCRUDRepository):
    @staticmethod
    def get_base_query(menu_id: UUID) -> Select:
        return select(Submenu).where(Submenu.menu_id == menu_id)

    @staticmethod
    async def get_by_id(
        menu_id: UUID, submenu_id: UUID, session: AsyncSession, orm_object: bool = False
    ) -> Row | Submenu | None:
        stmt = SubmenuRepository.get_base_query(menu_id).where(Submenu.id == submenu_id)
        result = await session.execute(stmt)
        if first := result.first():
            return first[0] if orm_object else first
        return None

    async def get(self, menu_id: UUID, submenu_id: UUID, session: AsyncSession) -> Row | None:
        stmt = self.get_base_query(menu_id).where(
            Submenu.id == submenu_id,
        )
        result = await session.execute(stmt)
        return result.first()

    async def all(self, menu_id: UUID, session: AsyncSession, scalar: bool = False) -> list[Row]:
        result = await session.execute(self.get_base_query(menu_id))
        return result.scalars().all() if scalar else result.all()

    async def create(self, menu: Menu, submenu: Submenu, session: AsyncSession, commit: bool = True) -> Row | None:
        menu.submenus.append(submenu)
        session.add(submenu)
        if commit is True:
            await session.commit()
            await session.refresh(submenu)
        return await self.get(submenu.menu_id, submenu.id, session)

    async def update(
        self,
        submenu: Submenu,
        updated_submenu: Submenu,
        session: AsyncSession,
        commit: bool = True,
    ) -> Row:
        updated_submenu_dict = updated_submenu.dict(exclude_unset=True)
        for key, val in updated_submenu_dict.items():
            setattr(submenu, key, val)

        if commit is True:
            await session.commit()
            await session.refresh(submenu)
        return await self.get(submenu.menu_id, submenu.id, session)  # type: ignore

    async def delete(self, submenu: Submenu, session: AsyncSession, commit: bool = True) -> None:
        if commit is True:
            await session.delete(submenu)
        await session.commit()


class SubmenuWithCountingRepository(SubmenuRepository):
    def get_base_query(self, menu_id: UUID) -> Select:  # type: ignore
        return (
            select(
                Submenu.id,
                Submenu.title,
                Submenu.description,
                func.count(distinct(Dish.id)).label('dishes_count'),
            )
            .outerjoin(Menu, Submenu.menu_id == Menu.id)
            .outerjoin(Dish, Dish.submenu_id == Submenu.id)
            .where(Menu.id == menu_id)
            .group_by(Submenu.id)
        )
