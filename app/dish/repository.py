from app.models import Submenu, Dish
from app.common.repository import BaseCRUDRepository
from app.submenu.repository import SUBMENU_NOT_FOUND_MESSAGE
from app.utils import get_first_or_404

DISH_NOT_FOUND_MESSAGE = "dish not found"


class DishRepository(BaseCRUDRepository):
    def retrieve(self, menu_id, submenu_id, dish_id, session):
        return get_first_or_404(
            Dish.select_by_id(menu_id, submenu_id, dish_id),
            session,
            DISH_NOT_FOUND_MESSAGE,
        )

    def list(self, menu_id, submenu_id, session):
        return session.exec(Dish.select_all(menu_id, submenu_id)).all()

    def create(self, menu_id, submenu_id, dish, session):
        submenu = get_first_or_404(
            Submenu.select_by_id(menu_id, submenu_id),
            session,
            SUBMENU_NOT_FOUND_MESSAGE,
        )
        submenu.dishes.append(dish)
        session.add(dish)
        session.commit()
        session.refresh(dish)
        return dish

    def update(self, menu_id, submenu_id, dish_id, updated_dish, session):
        dish = get_first_or_404(
            Dish.select_by_id(menu_id, submenu_id, dish_id),
            session,
            DISH_NOT_FOUND_MESSAGE,
        )

        updated_dish_dict = updated_dish.dict(exclude_unset=True)

        for key, val in updated_dish_dict.items():
            setattr(dish, key, val)

        session.add(dish)
        session.commit()
        session.refresh(dish)
        return dish

    def delete(self, menu_id, submenu_id, dish_id, session):
        dish = get_first_or_404(
            Dish.select_by_id(menu_id, submenu_id, dish_id),
            session,
            DISH_NOT_FOUND_MESSAGE,
        )

        session.delete(dish)
        session.commit()
        return {"status": True, "message": "The dish has been deleted"}
