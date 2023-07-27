from app.models import Menu
from app.utils import get_first_or_404

MENU_NOT_FOUND_MESSAGE = "menu not found"


class MenuService:

    @staticmethod
    def retrieve(menu_id, session):
        return get_first_or_404(
            Menu.select_by_id(menu_id), session, MENU_NOT_FOUND_MESSAGE
        )

    @staticmethod
    def list(session):
        return session.exec(Menu.select_all()).all()

    @staticmethod
    def create(menu, session):
        session.add(menu)
        session.commit()
        session.refresh(menu)
        return menu

    @staticmethod
    def update(menu_id, updated_menu, session):
        menu = get_first_or_404(
            Menu.select_by_id(menu_id), session, MENU_NOT_FOUND_MESSAGE
        )

        updated_menu_dict = updated_menu.dict(exclude_unset=True)
        for key, val in updated_menu_dict.items():
            setattr(menu, key, val)

        session.add(menu)
        session.commit()
        session.refresh(menu)
        return menu

    @staticmethod
    def delete(menu_id, session):
        menu = get_first_or_404(
            Menu.select_by_id(menu_id), session, MENU_NOT_FOUND_MESSAGE
        )
        session.delete(menu)
        session.commit()
        return {"status": True, "message": "The menu has been deleted"}
