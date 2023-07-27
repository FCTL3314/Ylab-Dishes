from app.models import Submenu, Dish
from app.common.repository import BaseCRUDRepository
from app.submenu.repository import SUBMENU_NOT_FOUND_MESSAGE
from app.utils import get_first_or_404

DISH_NOT_FOUND_MESSAGE = "dish not found"


class DishRepository(BaseCRUDRepository):
    def retrieve(self, menu_id, submenu_id, dish_id):
        return get_first_or_404(
            Dish.select_by_id(menu_id, submenu_id, dish_id),
            self.session,
            DISH_NOT_FOUND_MESSAGE,
        )

    def list(self, menu_id, submenu_id):
        return self.session.exec(Dish.select_all(menu_id, submenu_id)).all()

    def create(self, menu_id, submenu_id, dish):
        submenu = get_first_or_404(
            Submenu.select_by_id(menu_id, submenu_id),
            self.session,
            SUBMENU_NOT_FOUND_MESSAGE,
        )
        submenu.dishes.append(dish)
        self.session.add(dish)
        self.session.commit()
        self.session.refresh(dish)
        return dish

    def update(self, menu_id, submenu_id, dish_id, updated_dish):
        dish = get_first_or_404(
            Dish.select_by_id(menu_id, submenu_id, dish_id),
            self.session,
            DISH_NOT_FOUND_MESSAGE,
        )

        updated_dish_dict = updated_dish.dict(exclude_unset=True)

        for key, val in updated_dish_dict.items():
            setattr(dish, key, val)

        self.session.add(dish)
        self.session.commit()
        self.session.refresh(dish)
        return dish

    def delete(self, menu_id, submenu_id, dish_id):
        dish = get_first_or_404(
            Dish.select_by_id(menu_id, submenu_id, dish_id),
            self.session,
            DISH_NOT_FOUND_MESSAGE,
        )

        self.session.delete(dish)
        self.session.commit()
        return {"status": True, "message": "The dish has been deleted"}
