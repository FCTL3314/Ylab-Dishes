from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.repository import BaseCRUDRepository
from app.models import Dish, Submenu
from app.submenu.repository import SubmenuRepository
from app.utils import get_first_or_404

DISH_NOT_FOUND_MESSAGE = "dish not found"


class DishRepository(BaseCRUDRepository):
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
        result = await get_first_or_404(
            select(Dish)
            .join(Submenu, Dish.submenu_id == Submenu.id)
            .where(
                Submenu.menu_id == menu_id,
                Dish.submenu_id == submenu_id,
                Dish.id == dish_id,
            ),
            session,
            DISH_NOT_FOUND_MESSAGE,
        )
        return result[0] if orm_object else result

    async def retrieve(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: AsyncSession
    ):
        return await get_first_or_404(
            self.get_base_query(menu_id, submenu_id).where(Dish.id == dish_id),
            session,
            DISH_NOT_FOUND_MESSAGE,
        )

    async def list(self, menu_id: UUID, submenu_id: UUID, session: AsyncSession):
        result = await session.execute(self.get_base_query(menu_id, submenu_id))
        return result.all()

    async def create(
        self, menu_id: UUID, submenu_id: UUID, dish: Dish, session: AsyncSession
    ):
        submenu = await SubmenuRepository.get_by_id(
            menu_id, submenu_id, session, orm_object=True
        )
        submenu.dishes.append(dish)
        session.add(dish)
        await session.commit()
        await session.refresh(dish)
        return dish

    async def update(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        updated_dish: Dish,
        session: AsyncSession,
    ):
        dish = await self.get_by_id(
            menu_id, submenu_id, dish_id, session, orm_object=True
        )

        updated_dish_dict = updated_dish.dict(exclude_unset=True)

        for key, val in updated_dish_dict.items():
            setattr(dish, key, val)

        await session.commit()
        await session.refresh(dish)
        return dish

    async def delete(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: AsyncSession
    ):
        dish = await self.get_by_id(
            menu_id, submenu_id, dish_id, session, orm_object=True
        )

        await session.delete(dish)
        await session.commit()
        return {"status": True, "message": "The dish has been deleted"}
