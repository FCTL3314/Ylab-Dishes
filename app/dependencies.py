from fastapi import Depends

from app.db import get_async_session
from app.dish.repository import DishRepository
from app.dish.services import DishService
from app.menu.repository import MenuWithCountingRepository
from app.menu.services import CachedMenuService, MenuService
from app.submenu.repository import SubmenuWithCountingRepository
from app.submenu.services import SubmenuService

ActiveSession = Depends(get_async_session)


def menu_service():
    return MenuService(MenuWithCountingRepository())


ActiveMenuService = Depends(menu_service)


def cached_menu_service():
    return CachedMenuService(MenuWithCountingRepository())


ActiveCachedMenuService = Depends(cached_menu_service)


def submenu_service():
    return SubmenuService(SubmenuWithCountingRepository())


ActiveSubmenuService = Depends(submenu_service)


def dish_service():
    return DishService(DishRepository())


ActiveDishService = Depends(dish_service)
