from app.models import Dish, Submenu
from sqlmodel import select as sqlmodel_select
from app.common.repository import BaseCRUDRepository
from app.submenu.repository import SubmenuRepository
from app.utils import get_first_or_404

DISH_NOT_FOUND_MESSAGE = "dish not found"


class DishRepository(BaseCRUDRepository):

    @staticmethod
    def get_base_query(menu_id, submenu_id):
        return (
            sqlmodel_select(Dish)
            .join(Submenu, Dish.submenu_id == Submenu.id)
            .where(
                Dish.submenu_id == submenu_id,
                Submenu.menu_id == menu_id,
            )
        )

    @staticmethod
    def get_by_id(menu_id, submenu_id, dish_id, session):
        return get_first_or_404(
            DishRepository.get_base_query(menu_id, submenu_id).where(Dish.id == dish_id),
            session,
            DISH_NOT_FOUND_MESSAGE,
        )

    def retrieve(self, menu_id, submenu_id, dish_id):
        return get_first_or_404(
            self.get_base_query(menu_id, submenu_id).where(Dish.id == dish_id),
            self.session,
            DISH_NOT_FOUND_MESSAGE,
        )

    def list(self, menu_id, submenu_id):
        return self.session.exec(self.get_base_query(menu_id, submenu_id)).all()

    def create(self, menu_id, submenu_id, dish):
        submenu = SubmenuRepository.get_by_id(menu_id, submenu_id, self.session)
        submenu.dishes.append(dish)
        self.session.add(dish)
        self.session.commit()
        self.session.refresh(dish)
        return dish

    def update(self, menu_id, submenu_id, dish_id, updated_dish):
        dish = self.get_by_id(menu_id, submenu_id, dish_id, self.session)

        updated_dish_dict = updated_dish.dict(exclude_unset=True)

        for key, val in updated_dish_dict.items():
            setattr(dish, key, val)

        self.session.add(dish)
        self.session.commit()
        self.session.refresh(dish)
        return dish

    def delete(self, menu_id, submenu_id, dish_id):
        dish = self.get_by_id(menu_id, submenu_id, dish_id, self.session)

        self.session.delete(dish)
        self.session.commit()
        return {"status": True, "message": "The dish has been deleted"}
