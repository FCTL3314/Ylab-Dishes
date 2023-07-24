from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from sqlmodel import Session

from app.dependencies import ActiveSession
from app.menu.schemas import MenuResponse
from app.models import Menu
from app.utils import get_first_or_404

router = APIRouter()

MENU_NOT_FOUND_MESSAGE = "menu not found"


@router.get("/{menu_id}/", response_model=MenuResponse)
async def menu_retrieve(menu_id: UUID, session: Session = ActiveSession):
    menu = get_first_or_404(Menu.select_by_id(menu_id), session, MENU_NOT_FOUND_MESSAGE)
    return menu


@router.get("/", response_model=list[MenuResponse])
async def menu_list(session: Session = ActiveSession):
    menus = session.exec(Menu.select_all()).all()
    return menus


@router.post("/", response_model=MenuResponse, status_code=HTTPStatus.CREATED)
async def menu_create(menu: Menu, session: Session = ActiveSession):
    session.add(menu)
    session.commit()
    session.refresh(menu)
    return menu


@router.patch("/{menu_id}/", response_model=MenuResponse)
async def menu_patch(
        menu_id: UUID, updated_menu: Menu, session: Session = ActiveSession
):
    menu = get_first_or_404(Menu.select_by_id(menu_id), session, MENU_NOT_FOUND_MESSAGE)

    updated_menu_dict = updated_menu.dict(exclude_unset=True)
    for key, val in updated_menu_dict.items():
        setattr(menu, key, val)

    session.add(menu)
    session.commit()
    session.refresh(menu)
    return menu


@router.delete("/{menu_id}/")
async def menu_delete(menu_id: UUID, session: Session = ActiveSession):
    menu = get_first_or_404(Menu.select_by_id(menu_id), session, MENU_NOT_FOUND_MESSAGE)
    session.delete(menu)
    session.commit()
    return {"status": True, "message": "The menu has been deleted"}
