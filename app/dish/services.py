from sqlmodel import select

from app.models import Dish, Submenu


def get_dishes_query(menu_id, submenu_id):
    return (
        select(Dish)
        .join(Submenu, Dish.submenu_id == Submenu.id)
        .where(Dish.submenu_id == submenu_id, Submenu.menu_id == menu_id)
    )


def get_dish_by_id(menu_id, submenu_id, dish_id):
    return get_dishes_query(menu_id, submenu_id).where(Dish.id == dish_id)
