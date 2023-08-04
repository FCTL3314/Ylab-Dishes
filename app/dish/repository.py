from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.repository import AbstractCRUDRepository
from app.models import Dish, Submenu


class DishRepository(AbstractCRUDRepository):
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
    ) -> Dish:
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
    ) -> Row:
        stmt = self.get_base_query(menu_id, submenu_id).where(Dish.id == dish_id)
        result = await session.execute(stmt)
        return result.first()

    async def all(
        self, menu_id: UUID, submenu_id: UUID, session: AsyncSession
    ) -> list[Row]:
        result = await session.execute(self.get_base_query(menu_id, submenu_id))
        return result.all()

    @staticmethod
    async def create(submenu: Submenu, dish: Dish, session: AsyncSession) -> Dish:
        submenu.dishes.append(dish)
        session.add(dish)
        await session.commit()
        await session.refresh(dish)
        return dish

    @staticmethod
    async def update(dish: Dish, updated_dish: Dish, session: AsyncSession) -> Dish:
        updated_dish_dict = updated_dish.dict(exclude_unset=True)

        for key, val in updated_dish_dict.items():
            setattr(dish, key, val)

        await session.commit()
        await session.refresh(dish)
        return dish

    @staticmethod
    async def delete(dish: Dish, session: AsyncSession) -> dict:
        await session.delete(dish)
        await session.commit()
        return {"status": True, "message": "The dish has been deleted"}
