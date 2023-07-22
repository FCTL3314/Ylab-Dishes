from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from http import HTTPStatus

from app.db import ActiveSession
from app.dish.models import Menu, Submenu
from app.utils import get_object_or_404

router = APIRouter()

MENU_NOT_FOUND_MESSAGE = "menu not found"
SUBMENU_NOT_FOUND_MESSAGE = "submenu not found"
DISH_NOT_FOUND_MESSAGE = "dish not found"


@router.get('/menus/{menu_id}/')
def menu_retrieve(menu_id: UUID, session: Session = ActiveSession):
    menu = get_object_or_404(Menu, menu_id, session, not_found_msg=MENU_NOT_FOUND_MESSAGE)

    return {
        **menu.dict(),
        "submenus_count": menu.submenus_count,
        "dishes_count": menu.dishes_count,
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


@router.get('/menus/{menu_id}/submenus/{submenu_id}/')
def submenu_retrieve(menu_id: UUID, submenu_id: UUID, session: Session = ActiveSession):
    menu = get_object_or_404(Menu, menu_id, session, not_found_msg=MENU_NOT_FOUND_MESSAGE)
    submenu = next((submenu for submenu in menu.submenus if submenu.id == submenu_id), None)

    if submenu is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=SUBMENU_NOT_FOUND_MESSAGE)

    return {
        **submenu.dict(),
        "dishes_count": submenu.dishes_count,
    }


@router.get("/menus/{menu_id}/submenus/", response_model=list[Submenu])
def submenu_list(menu_id: UUID, session: Session = ActiveSession):
    menu = get_object_or_404(Menu, menu_id, session, not_found_msg=MENU_NOT_FOUND_MESSAGE)
    return menu.submenus


@router.post("/menus/{menu_id}/submenus/", response_model=Submenu, status_code=HTTPStatus.CREATED)
def submenu_create(menu_id: UUID, submenu: Submenu, session: Session = ActiveSession):
    menu = get_object_or_404(Menu, menu_id, session, not_found_msg=MENU_NOT_FOUND_MESSAGE)
    menu.submenus.append(submenu)
    session.add(submenu)
    session.commit()
    session.refresh(submenu)
    return submenu


@router.patch('/menus/{menu_id}/submenus/{submenu_id}/')
def submenu_patch(menu_id: UUID, submenu_id: UUID, updated_submenu: Menu, session: Session = ActiveSession):
    menu = get_object_or_404(Menu, menu_id, session, not_found_msg=MENU_NOT_FOUND_MESSAGE)
    submenu = next((submenu for submenu in menu.submenus if submenu.id == submenu_id), None)

    if submenu is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=SUBMENU_NOT_FOUND_MESSAGE)

    updated_submenu_dict = updated_submenu.dict(exclude_unset=True)
    for key, val in updated_submenu_dict.items():
        setattr(submenu, key, val)

    session.add(submenu)
    session.commit()
    session.refresh(submenu)
    return {
        **submenu.dict(),
        "dishes_count": submenu.dishes_count,
    }


@router.delete("/menus/{menu_id}/submenus/{submenu_id}/")
def menu_delete(menu_id: UUID, submenu_id: UUID, session: Session = ActiveSession):
    menu = get_object_or_404(Menu, menu_id, session, not_found_msg=MENU_NOT_FOUND_MESSAGE)
    submenu = next((submenu for submenu in menu.submenus if submenu.id == submenu_id), None)

    if submenu is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=SUBMENU_NOT_FOUND_MESSAGE)

    session.delete(submenu)
    session.commit()
    return {"status": True, "message": "The submenu has been deleted"}
