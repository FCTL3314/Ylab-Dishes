from fastapi import Depends

from app.db import get_async_session
from app.dish.repository import DishRepository
from app.dish.services import DishService
from app.menu.repository import MenuWithCountingRepository
from app.menu.services import MenuService
from app.submenu.repository import SubmenuWithCountingRepository
from app.submenu.services import SubmenuService

ActiveSession = Depends(get_async_session)
ActiveMenuService = Depends(lambda: MenuService(MenuWithCountingRepository))
ActiveSubmenuService = Depends(lambda: SubmenuService(SubmenuWithCountingRepository))
ActiveDishService = Depends(lambda: DishService(DishRepository))
