from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from sqlmodel import Session

from app.dependencies import ActiveSession
from app.menu.routes import MENU_NOT_FOUND_MESSAGE
from app.models import Menu, Submenu
from app.submenu.schemas import SubmenuResponse
from app.utils import get_first_or_404

router = APIRouter()

SUBMENU_NOT_FOUND_MESSAGE = "submenu not found"


@router.get("/{submenu_id}/", response_model=SubmenuResponse)
async def submenu_retrieve(
        menu_id: UUID, submenu_id: UUID, session: Session = ActiveSession
):
    submenu = get_first_or_404(
        Submenu.select_by_id(menu_id, submenu_id),
        session,
        SUBMENU_NOT_FOUND_MESSAGE,
    )
    return submenu


@router.get("/", response_model=list[SubmenuResponse])
async def submenu_list(menu_id: UUID, session: Session = ActiveSession):
    return session.exec(Submenu.select_all(menu_id)).all()


@router.post("/", response_model=SubmenuResponse, status_code=HTTPStatus.CREATED)
async def submenu_create(
        menu_id: UUID, submenu: Submenu, session: Session = ActiveSession
):
    menu = get_first_or_404(
        Menu.select_by_id(menu_id),
        session,
        MENU_NOT_FOUND_MESSAGE,
    )
    menu.submenus.append(submenu)
    session.add(submenu)
    session.commit()
    session.refresh(submenu)
    return submenu


@router.patch("/{submenu_id}/", response_model=SubmenuResponse)
async def submenu_patch(
        menu_id: UUID,
        submenu_id: UUID,
        updated_submenu: Menu,
        session: Session = ActiveSession,
):
    submenu = get_first_or_404(
        Submenu.select_by_id(menu_id, submenu_id),
        session,
        SUBMENU_NOT_FOUND_MESSAGE,
    )
    updated_submenu_dict = updated_submenu.dict(exclude_unset=True)
    for key, val in updated_submenu_dict.items():
        setattr(submenu, key, val)
    session.add(submenu)
    session.commit()
    session.refresh(submenu)
    return submenu


@router.delete("/{submenu_id}/")
async def submenu_delete(
        menu_id: UUID, submenu_id: UUID, session: Session = ActiveSession
):
    submenu = get_first_or_404(
        Submenu.select_by_id(menu_id, submenu_id),
        session,
        SUBMENU_NOT_FOUND_MESSAGE,
    )
    session.delete(submenu)
    session.commit()
    return {"status": True, "message": "The submenu has been deleted"}
