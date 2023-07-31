from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.repository import AbstractRepository
from app.models import Dish, Submenu

DISH_NOT_FOUND_MESSAGE = "dish not found"


class DishRepository(AbstractRepository):
    @staticmethod
    def get_base_query(menu_id: UUID, submenu_id: UUID):
        return (
            select(
                Dish.id,
                Dish.title,
                Dish.description,
                Dish.price,
                Dish.submenu_id,
            )
            .join(Submenu, Dish.submenu_id == Submenu.id)
            .where(
                Dish.submenu_id == submenu_id,
                Submenu.menu_id == menu_id,
            )
        )

    @staticmethod
    async def get_by_id(
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        session: AsyncSession,
        orm_object: bool = False,
    ):
        stmt = (
            select(Dish)
            .join(Submenu, Dish.submenu_id == Submenu.id)
            .where(
                Submenu.menu_id == menu_id,
                Dish.submenu_id == submenu_id,
                Dish.id == dish_id,
            )
        )
        result = await session.execute(stmt)
        return result.first()[0] if orm_object else result.first()

    async def get(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: AsyncSession
    ):
        stmt = self.get_base_query(menu_id, submenu_id).where(Dish.id == dish_id)
        result = await session.execute(stmt)
        return result.first()

    async def all(self, menu_id: UUID, submenu_id: UUID, session: AsyncSession):
        result = await session.execute(self.get_base_query(menu_id, submenu_id))
        return result.all()

    async def create(self, submenu: Submenu, dish: Dish, session: AsyncSession):
        submenu.dishes.append(dish)
        session.add(dish)
        await session.commit()
        await session.refresh(dish)
        return dish

    async def update(self, dish: Dish, updated_dish: Dish, session: AsyncSession):
        updated_dish_dict = updated_dish.dict(exclude_unset=True)

        for key, val in updated_dish_dict.items():
            setattr(dish, key, val)

        await session.commit()
        await session.refresh(dish)
        return dish

    async def delete(self, dish: Dish, session: AsyncSession):
        await session.delete(dish)
        await session.commit()
        return {"status": True, "message": "The dish has been deleted"}
