from fastapi import Depends

from app.db import get_async_session
from app.menu.repository import MenuRepository, MenuWithCountingRepository
from app.menu.services import MenuService
from app.submenu.repository import SubmenuWithCountingRepository
from app.submenu.services import SubmenuService

ActiveSession = Depends(get_async_session)
ActiveMenuService = Depends(lambda: MenuService(MenuWithCountingRepository))
ActiveSubmenuService = Depends(
    lambda: SubmenuService(MenuWithCountingRepository, SubmenuWithCountingRepository)
)
