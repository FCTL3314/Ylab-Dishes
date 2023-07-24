from sqlmodel import select

from app.models import Menu


def get_menus_query():
    return select(Menu)


def get_menu_by_id(menu_id):
    return get_menus_query().where(Menu.id == menu_id)
