from uuid import UUID

from sqlalchemy import distinct, func, select

from app.common.repository import AbstractCRUDRepository
from app.models import Dish, Menu, Submenu


class MenuRepository(AbstractCRUDRepository):
    base_query = select(Menu)

    @staticmethod
    async def get_by_id(menu_id: UUID, session, orm_object: bool = False):
        stmt = select(Menu).where(Menu.id == menu_id)
        result = await session.execute(stmt)
        return result.first()[0] if orm_object else result.first()

    async def retrieve(self, menu_id: UUID, session):
        stmt = self.base_query.where(Menu.id == menu_id)
        res = await session.execute(stmt)
        return res.first()

    async def list(self, session):
        result = await session.execute(self.base_query)
        return result.all()

    async def create(self, menu: Menu, session):
        session.add(menu)
        await session.commit()
        await session.refresh(menu)
        return await self.retrieve(menu.id, session)

    async def update(self, menu: Menu, updated_menu: Menu, session):
        updated_menu_dict = updated_menu.dict(exclude_unset=True)

        for key, val in updated_menu_dict.items():
            setattr(menu, key, val)

        await session.commit()
        await session.refresh(menu)
        return await self.retrieve(menu.id, session)

    async def delete(self, menu: Menu, session):
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
