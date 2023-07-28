from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from sqlmodel import Session

from app.dependencies import ActiveSession
from app.models import Menu, Submenu
from app.submenu.repository import SubmenuWithCountingRepository
from app.submenu.schemas import SubmenuResponse

router = APIRouter()


submenu_repository = SubmenuWithCountingRepository()


@router.get("/{submenu_id}/", response_model=SubmenuResponse)
async def submenu_retrieve(menu_id: UUID, submenu_id: UUID):
    return submenu_repository.retrieve(menu_id, submenu_id)


@router.get("/", response_model=list[SubmenuResponse])
async def submenu_list(menu_id: UUID):
    return submenu_repository.list(menu_id)


@router.post("/", response_model=SubmenuResponse, status_code=HTTPStatus.CREATED)
async def submenu_create(menu_id: UUID, submenu: Submenu):
    return submenu_repository.create(menu_id, submenu)


@router.patch("/{submenu_id}/", response_model=SubmenuResponse)
async def submenu_patch(
    menu_id: UUID,
    submenu_id: UUID,
    updated_submenu: Menu,
):
    return submenu_repository.update(menu_id, submenu_id, updated_submenu)


@router.delete("/{submenu_id}/")
async def submenu_delete(menu_id: UUID, submenu_id: UUID):
    return submenu_repository.delete(menu_id, submenu_id)
