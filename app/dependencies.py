from fastapi import Depends

from app.db import get_async_session
from app.menu.repository import MenuWithCountingRepository
from app.menu.services import MenuService

ActiveSession = Depends(get_async_session)
ActiveMenuService = Depends(lambda: MenuService(MenuWithCountingRepository))
