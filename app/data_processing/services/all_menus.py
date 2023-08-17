from sqlalchemy.ext.asyncio import AsyncSession

from app.common.services import AbstractListService
from app.menu.dependencies import menu_nested_service
from app.menu.schemas import MenuNestedResponse

TASK_NOT_FOUND_MESSAGE = 'Task not found or still being processing.'


class AllMenusService(AbstractListService):
    """
    Service for getting all menus with all nested submenus and dishes.
    """
    async def list(self, session: AsyncSession) -> list[MenuNestedResponse]:
        return await menu_nested_service().list(session, scalar=True)
