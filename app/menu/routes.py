from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from sqlmodel import Session

from app.dependencies import ActiveSession
from app.menu.repository import MenuRepository
from app.menu.schemas import MenuResponse
from app.models import Menu

router = APIRouter()


menu_repository = MenuRepository()


@router.get("/{menu_id}/", response_model=MenuResponse)
async def menu_retrieve(menu_id: UUID, session: Session = ActiveSession):
    return menu_repository.retrieve(menu_id, session)


@router.get("/", response_model=list[MenuResponse])
async def menu_list(session: Session = ActiveSession):
    return menu_repository.list(session)


@router.post("/", response_model=MenuResponse, status_code=HTTPStatus.CREATED)
async def menu_create(menu: Menu, session: Session = ActiveSession):
    return menu_repository.create(menu, session)


@router.patch("/{menu_id}/", response_model=MenuResponse)
async def menu_patch(
    menu_id: UUID, updated_menu: Menu, session: Session = ActiveSession
):
    return menu_repository.update(menu_id, updated_menu, session)


@router.delete("/{menu_id}/")
async def menu_delete(menu_id: UUID, session: Session = ActiveSession):
    return menu_repository.delete(menu_id, session)
