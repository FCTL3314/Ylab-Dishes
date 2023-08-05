from fastapi import Depends

from app.db import get_async_session
from app.dish.repository import DishRepository
from app.dish.schemas import DishBase
from app.dish.services import CachedDishService, DishService
from app.menu.repository import MenuWithCountingRepository
from app.menu.schemas import MenuResponse
from app.menu.services import CachedMenuService, MenuService
from app.submenu.repository import SubmenuWithCountingRepository
from app.submenu.schemas import SubmenuResponse
from app.submenu.services import CachedSubmenuService, SubmenuService

ActiveSession = Depends(get_async_session)


def menu_service():
    return MenuService[MenuResponse](MenuWithCountingRepository())


ActiveMenuService = Depends(menu_service)


def cached_menu_service():
    return CachedMenuService[MenuResponse](MenuWithCountingRepository())


ActiveCachedMenuService = Depends(cached_menu_service)


def submenu_service():
    return SubmenuService[SubmenuResponse](SubmenuWithCountingRepository())


ActiveSubmenuService = Depends(submenu_service)


def cached_submenu_service():
    return CachedSubmenuService[SubmenuResponse](SubmenuWithCountingRepository())


ActiveCachedSubmenuService = Depends(cached_submenu_service)


def dish_service():
    return DishService[DishBase](DishRepository())


ActiveDishService = Depends(dish_service)


def cached_dish_service():
    return CachedDishService[DishBase](DishRepository())


ActiveCachedDishService = Depends(cached_dish_service)
