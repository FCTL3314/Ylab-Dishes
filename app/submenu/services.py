from sqlmodel import select

from app.models import Submenu, Menu


def get_submenus_query(menu_id):
    return select(Submenu).where(Menu.id == menu_id)


def get_submenu_by_id(menu_id, submenu_id):
    return get_submenus_query(menu_id).where(Submenu.id == submenu_id)
