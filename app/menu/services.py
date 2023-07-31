from http import HTTPStatus
from fastapi import HTTPException
from uuid import UUID

from app.db import async_session_maker

MENU_NOT_FOUND_MESSAGE = "menu not found"


class MenuService:
    def __init__(self, repository):
        self.repository = repository

    @staticmethod
    def _is_menu_exists_or_404(menu):
        if not menu:
            raise HTTPException(
                detail=MENU_NOT_FOUND_MESSAGE, status_code=HTTPStatus.NOT_FOUND
            )

    async def retrieve(self, menu_id: UUID):
        async with async_session_maker() as session:
            menu = await self.repository().retrieve(menu_id, session)
            self._is_menu_exists_or_404(menu)
            return menu

    async def list(self):
        async with async_session_maker() as session:
            return await self.repository().list(session)

    async def create(self, menu):
        async with async_session_maker() as session:
            return await self.repository().create(menu, session)

    async def update(self, menu_id, updated_menu):
        async with async_session_maker() as session:
            menu = await self.repository().get_by_id(menu_id, session, orm_object=True)
            self._is_menu_exists_or_404(menu)
            return await self.repository().update(menu, updated_menu, session)

    async def delete(self, menu_id):
        async with async_session_maker() as session:
            menu = await self.repository().get_by_id(menu_id, session, orm_object=True)
            self._is_menu_exists_or_404(menu)
            return await self.repository().delete(menu, session)
