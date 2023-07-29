from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import ActiveSession
from app.menu.repository import MenuWithCountingRepository
from app.menu.schemas import MenuResponse
from app.models import Menu

router = APIRouter()

menu_repository = MenuWithCountingRepository()


@router.get("/{menu_id}/")
async def menu_retrieve(menu_id: UUID, session: AsyncSession = ActiveSession):
    response = await menu_repository.retrieve(menu_id, session)
    return response


@router.get("/", response_model=list[MenuResponse])
async def menu_list(session: AsyncSession = ActiveSession):
    response = await menu_repository.list(session)
    return response


@router.post("/", response_model=MenuResponse, status_code=HTTPStatus.CREATED)
async def menu_create(menu: Menu, session: AsyncSession = ActiveSession):
    response = await menu_repository.create(menu, session)
    return response


@router.patch("/{menu_id}/", response_model=MenuResponse)
async def menu_patch(
    menu_id: UUID, updated_menu: Menu, session: AsyncSession = ActiveSession
):
    response = await menu_repository.update(menu_id, updated_menu, session)
    return response


@router.delete("/{menu_id}/")
async def menu_delete(menu_id: UUID, session: AsyncSession = ActiveSession):
    response = await menu_repository.delete(menu_id, session)
    return response
