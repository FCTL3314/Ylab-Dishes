from sqlalchemy import distinct, func, select
from sqlmodel import select as sqlmodel_select

from app.common.repository import BaseCRUDRepository
from app.models import Dish, Menu, Submenu
from app.utils import get_first_or_404

MENU_NOT_FOUND_MESSAGE = "menu not found"


class MenuRepository(BaseCRUDRepository):
    base_query = sqlmodel_select(Menu)

    @staticmethod
    def get_by_id(menu_id, session):
        return get_first_or_404(
            sqlmodel_select(Menu).where(Menu.id == menu_id),
            session,
            MENU_NOT_FOUND_MESSAGE,
        )

    def retrieve(self, menu_id, session):
        query = self.base_query.where(Menu.id == menu_id)
        return get_first_or_404(query, session, MENU_NOT_FOUND_MESSAGE)

    def list(self, session):
        return session.exec(self.base_query).all()

    def create(self, menu, session):
        session.add(menu)
        session.commit()
        session.refresh(menu)
        return self.retrieve(menu.id, session)

    def update(self, menu_id, updated_menu, session):
        menu = self.get_by_id(menu_id, session)

        updated_menu_dict = updated_menu.dict(exclude_unset=True)
        for key, val in updated_menu_dict.items():
            setattr(menu, key, val)

        session.add(menu, session)
        session.commit()
        session.refresh(menu)
        return self.retrieve(menu_id, session)

    def delete(self, menu_id, session):
        menu = self.get_by_id(menu_id, session)
        session.delete(menu)
        session.commit()
        return {"status": True, "message": "The menu has been deleted"}


class MenuWithCountingRepository(MenuRepository):
    base_query = (
        select(
            Menu.id,
            Menu.title,
            Menu.description,
            func.count(distinct(Submenu.id)).label("submenus_count"),
            func.count(distinct(Dish.id)).label("dishes_count"),
        )
        .outerjoin(Submenu, Submenu.menu_id == Menu.id)
        .outerjoin(Dish, Dish.submenu_id == Submenu.id)
        .group_by(Menu.id)
    )