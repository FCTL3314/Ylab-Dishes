from app.common.repository import BaseCRUDRepository
from app.models import Menu
from app.utils import get_first_or_404

MENU_NOT_FOUND_MESSAGE = "menu not found"


class MenuRepository(BaseCRUDRepository):
    def retrieve(self, menu_id):
        query = Menu.select_all_with_count().where(Menu.id == menu_id)
        return get_first_or_404(query, self.session, MENU_NOT_FOUND_MESSAGE)

    def list(self, session):
        return session.exec(Menu.select_all_with_count()).all()

    def create(self, menu):
        self.session.add(menu)
        self.session.commit()
        self.session.refresh(menu)
        return self.retrieve(menu.id)

    def update(self, menu_id, updated_menu):
        menu = get_first_or_404(
            Menu.select_by_id(menu_id), self.session, MENU_NOT_FOUND_MESSAGE
        )

        updated_menu_dict = updated_menu.dict(exclude_unset=True)
        for key, val in updated_menu_dict.items():
            setattr(menu, key, val)

        self.session.add(menu)
        self.session.commit()
        self.session.refresh(menu)
        return self.retrieve(menu_id)

    def delete(self, menu_id):
        menu = get_first_or_404(
            Menu.select_by_id(menu_id), self.session, MENU_NOT_FOUND_MESSAGE
        )
        self.session.delete(menu)
        self.session.commit()
        return {"status": True, "message": "The menu has been deleted"}
