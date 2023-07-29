from uuid import UUID

from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.repository import BaseCRUDRepository
from app.models import Dish, Menu, Submenu
from app.utils import get_first_or_404

MENU_NOT_FOUND_MESSAGE = "menu not found"


class MenuRepository(BaseCRUDRepository):
    base_query = select(Menu)

    @staticmethod
    async def get_by_id(menu_id: UUID, session: AsyncSession, orm_object: bool = False):
        result = await get_first_or_404(
            select(Menu).where(Menu.id == menu_id),
            session,
            MENU_NOT_FOUND_MESSAGE,
        )
        return result[0] if orm_object else result

    async def retrieve(self, menu_id: UUID, session: AsyncSession):
        query = self.base_query.where(Menu.id == menu_id)
        return await get_first_or_404(query, session, MENU_NOT_FOUND_MESSAGE)

    async def list(self, session: AsyncSession):
        result = await session.execute(self.base_query)
        return result.all()

    async def create(self, menu: Menu, session: AsyncSession):
        session.add(menu)
        await session.commit()
        await session.refresh(menu)
        return await self.retrieve(menu.id, session)

    async def update(self, menu_id: UUID, updated_menu: Menu, session: AsyncSession):
        menu = await self.get_by_id(menu_id, session, orm_object=True)

        updated_menu_dict = updated_menu.dict(exclude_unset=True)
        for key, val in updated_menu_dict.items():
            setattr(menu, key, val)

        await session.commit()
        await session.refresh(menu)
        return await self.retrieve(menu_id, session)

    async def delete(self, menu_id: UUID, session: AsyncSession):
        menu = await self.get_by_id(menu_id, session, orm_object=True)
        await session.delete(menu)
        await session.commit()
        return {"status": True, "message": "The menu has been deleted"}


class MenuWithCountingRepository(MenuRepository):
    base_query = (
        select(
            Menu.id,
            Menu.title,
            Menu.description,
            func.count(distinct(Submenu.id)).label("submenus_count"),
            func.count(distinct(Dish.id)).label("dishes_count"),
        )
        .outerjoin(Submenu, Submenu.menu_id == Menu.id)
        .outerjoin(Dish, Dish.submenu_id == Submenu.id)
        .group_by(Menu.id)
    )
