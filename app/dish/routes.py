from uuid import UUID

from fastapi import APIRouter
from sqlmodel import Session, select
from http import HTTPStatus

from app.db import ActiveSession
from app.dish.models import Menu
from app.utils import get_object_or_404

router = APIRouter()

MENU_NOT_FOUND_MESSAGE = "menu not found"


@router.get('/menus/{menu_id}/')
def menu_retrieve(menu_id: UUID, session: Session = ActiveSession):
    menu = get_object_or_404(Menu, menu_id, session, not_found_msg=MENU_NOT_FOUND_MESSAGE)

    return {
        **menu.dict(),
        "submenus_count": menu.submenus_count,
    }


@router.get("/menus/", response_model=list[Menu])
def menu_list(session: Session = ActiveSession):
    statement = select(Menu)
    menus = session.exec(statement).all()
    return menus


@router.post("/menus/", response_model=Menu, status_code=HTTPStatus.CREATED)
def menu_create(menu: Menu, session: Session = ActiveSession):
    session.add(menu)
    session.commit()
    session.refresh(menu)
    return menu


@router.patch('/menus/{menu_id}/')
def menu_patch(menu_id: UUID, updated_menu: Menu, session: Session = ActiveSession):
    menu = get_object_or_404(Menu, menu_id, session, not_found_msg=MENU_NOT_FOUND_MESSAGE)

    updated_menu_dict = updated_menu.dict(exclude_unset=True)
    for key, val in updated_menu_dict.items():
        setattr(menu, key, val)

    session.add(menu)
    session.commit()
    session.refresh(menu)
    return {
        **menu.dict(),
        "submenus_count": menu.submenus_count,
    }


@router.delete("/menus/{menu_id}/")
def menu_delete(menu_id: UUID, session: Session = ActiveSession):
    menu = get_object_or_404(Menu, menu_id, session, not_found_msg=MENU_NOT_FOUND_MESSAGE)
    session.delete(menu)
    session.commit()
    return {"status": True, "message": "The menu has been deleted"}
