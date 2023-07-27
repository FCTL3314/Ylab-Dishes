from app.common.repository import BaseCRUDRepository
from app.menu.repository import MENU_NOT_FOUND_MESSAGE
from app.models import Submenu, Menu
from app.utils import get_first_or_404

SUBMENU_NOT_FOUND_MESSAGE = "submenu not found"


class SubmenuRepository(BaseCRUDRepository):
    def retrieve(self, menu_id, submenu_id, session):
        query = Submenu.query_with_count(menu_id).where(
            Submenu.id == submenu_id,
        )
        return get_first_or_404(
            query,
            session,
            SUBMENU_NOT_FOUND_MESSAGE,
        )

    def list(self, menu_id, session):
        return session.exec(Submenu.query_with_count(menu_id)).all()

    def create(self, menu_id, submenu, session):
        menu = get_first_or_404(
            Menu.select_by_id(menu_id),
            session,
            MENU_NOT_FOUND_MESSAGE,
        )
        menu.submenus.append(submenu)
        session.add(submenu)
        session.commit()
        session.refresh(submenu)
        return self.retrieve(menu_id, submenu.id, session)

    def update(self, menu_id, submenu_id, updated_submenu, session):
        submenu = get_first_or_404(
            Submenu.select_by_id(menu_id, submenu_id),
            session,
            SUBMENU_NOT_FOUND_MESSAGE,
        )
        updated_submenu_dict = updated_submenu.dict(exclude_unset=True)
        for key, val in updated_submenu_dict.items():
            setattr(submenu, key, val)
        session.add(submenu)
        session.commit()
        session.refresh(submenu)
        return self.retrieve(menu_id, submenu.id, session)

    def delete(self, menu_id, submenu_id, session):
        submenu = get_first_or_404(
            Submenu.select_by_id(menu_id, submenu_id),
            session,
            SUBMENU_NOT_FOUND_MESSAGE,
        )
        session.delete(submenu)
        session.commit()
        return {"status": True, "message": "The submenu has been deleted"}
