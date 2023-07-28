from sqlalchemy import func, distinct, select
from sqlmodel import select as sqlmodel_select

from app.common.repository import BaseCRUDRepository
from app.menu.repository import MenuRepository
from app.models import Submenu, Menu, Dish
from app.utils import get_first_or_404

SUBMENU_NOT_FOUND_MESSAGE = "submenu not found"


class SubmenuRepository(BaseCRUDRepository):

    @staticmethod
    def get_base_query(menu_id):
        return sqlmodel_select(Submenu).where(Submenu.menu_id == menu_id)

    @staticmethod
    def get_by_id(menu_id, submenu_id, session):
        return get_first_or_404(
            SubmenuRepository.get_base_query(menu_id).where(Submenu.id == submenu_id),
            session,
            SUBMENU_NOT_FOUND_MESSAGE,
        )

    def retrieve(self, menu_id, submenu_id):
        query = self.get_base_query(menu_id).where(
            Submenu.id == submenu_id,
        )
        return get_first_or_404(
            query,
            self.session,
            SUBMENU_NOT_FOUND_MESSAGE,
        )

    def list(self, menu_id):
        return self.session.exec(self.get_base_query(menu_id)).all()

    def create(self, menu_id, submenu):
        menu = MenuRepository.get_by_id(menu_id, self.session)
        menu.submenus.append(submenu)
        self.session.add(submenu)
        self.session.commit()
        self.session.refresh(submenu)
        return self.retrieve(menu_id, submenu.id)

    def update(self, menu_id, submenu_id, updated_submenu):
        submenu = self.get_by_id(menu_id, submenu_id, self.session)
        updated_submenu_dict = updated_submenu.dict(exclude_unset=True)
        for key, val in updated_submenu_dict.items():
            setattr(submenu, key, val)
        self.session.add(submenu)
        self.session.commit()
        self.session.refresh(submenu)
        return self.retrieve(menu_id, submenu.id)

    def delete(self, menu_id, submenu_id):
        submenu = self.get_by_id(menu_id, submenu_id, self.session)
        self.session.delete(submenu)
        self.session.commit()
        return {"status": True, "message": "The submenu has been deleted"}


class SubmenuWithCountingRepository(SubmenuRepository):
    def get_base_query(self, menu_id):
        return (
            select(
                Submenu.id,
                Submenu.title,
                Submenu.description,
                func.count(distinct(Dish.id)).label("dishes_count"),
            )
            .outerjoin(Menu, Submenu.menu_id == Menu.id)
            .outerjoin(Dish, Dish.submenu_id == Submenu.id)
            .where(Menu.id == menu_id)
            .group_by(Submenu.id)
        )
