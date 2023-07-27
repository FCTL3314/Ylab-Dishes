from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from sqlmodel import Session

from app.dependencies import ActiveSession
from app.models import Menu, Submenu
from app.submenu.schemas import SubmenuResponse
from app.submenu.services import SubmenuService

router = APIRouter()

SUBMENU_NOT_FOUND_MESSAGE = "submenu not found"


@router.get("/{submenu_id}/", response_model=SubmenuResponse)
async def submenu_retrieve(
    menu_id: UUID, submenu_id: UUID, session: Session = ActiveSession
):
    return SubmenuService.retrieve(menu_id, submenu_id, session)


@router.get("/", response_model=list[SubmenuResponse])
async def submenu_list(menu_id: UUID, session: Session = ActiveSession):
    return SubmenuService.list(menu_id, session)


@router.post("/", response_model=SubmenuResponse, status_code=HTTPStatus.CREATED)
async def submenu_create(
    menu_id: UUID, submenu: Submenu, session: Session = ActiveSession
):
    return SubmenuService.create(menu_id, submenu, session)


@router.patch("/{submenu_id}/", response_model=SubmenuResponse)
async def submenu_patch(
    menu_id: UUID,
    submenu_id: UUID,
    updated_submenu: Menu,
    session: Session = ActiveSession,
):
    return SubmenuService.update(menu_id, submenu_id, updated_submenu, session)


@router.delete("/{submenu_id}/")
async def submenu_delete(
    menu_id: UUID, submenu_id: UUID, session: Session = ActiveSession
):
    return SubmenuService.delete(menu_id, submenu_id, session)
