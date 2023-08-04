from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.services import AbstractCRUDService
from app.models import Dish
from app.submenu.repository import SubmenuRepository
from app.submenu.services import SUBMENU_NOT_FOUND_MESSAGE
from app.utils import is_obj_exists_or_404

DISH_NOT_FOUND_MESSAGE = "dish not found"


class DishService(AbstractCRUDService):
    async def retrieve(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: AsyncSession
    ) -> Dish:
        dish = await self.repository.get(menu_id, submenu_id, dish_id, session)
        is_obj_exists_or_404(dish, DISH_NOT_FOUND_MESSAGE)
        return dish

    async def list(
        self, menu_id: UUID, submenu_id: UUID, session: AsyncSession
    ) -> list[Dish]:
        return await self.repository.all(menu_id, submenu_id, session)

    async def create(
        self, menu_id: UUID, submenu_id: UUID, dish: Dish, session: AsyncSession
    ) -> Dish:
        submenu = await SubmenuRepository.get_by_id(
            menu_id, submenu_id, session, orm_object=True
        )
        is_obj_exists_or_404(submenu, SUBMENU_NOT_FOUND_MESSAGE)
        return await self.repository.create(submenu, dish, session)

    async def update(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        updated_dish: Dish,
        session: AsyncSession,
    ) -> Dish:
        dish = await self.repository.get_by_id(
            menu_id, submenu_id, dish_id, session, orm_object=True
        )
        is_obj_exists_or_404(dish, DISH_NOT_FOUND_MESSAGE)
        return await self.repository.update(dish, updated_dish, session)

    async def delete(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: AsyncSession
    ) -> dict:
        dish = await self.repository.get_by_id(
            menu_id, submenu_id, dish_id, session, orm_object=True
        )
        return await self.repository.delete(dish, session)
