from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from sqlmodel import Session, select

from app.db import ActiveSession
from app.menu.routes import MENU_NOT_FOUND_MESSAGE, get_menu_by_id_query
from app.models import Menu, Submenu
from app.utils import get_object_or_404

router = APIRouter()

SUBMENU_NOT_FOUND_MESSAGE = "submenu not found"


def get_submenu_query(menu_id, submenu_id):
    return (
        select(Submenu)
        .select_from(Menu)
        .where(
            Menu.id == menu_id,
            Submenu.id == submenu_id,
        )
    )


@router.get("/{submenu_id}/")
def submenu_retrieve(menu_id: UUID, submenu_id: UUID, session: Session = ActiveSession):
    query = get_submenu_query(menu_id, submenu_id)
    submenu = get_object_or_404(query, session, SUBMENU_NOT_FOUND_MESSAGE)

    return {
        **submenu.dict(),
        "dishes_count": submenu.dishes_count,
    }


@router.get("/", response_model=list[Submenu])
def submenu_list(menu_id: UUID, session: Session = ActiveSession):
    menu = get_object_or_404(
        get_menu_by_id_query(menu_id),
        session,
        MENU_NOT_FOUND_MESSAGE,
    )
    return menu.submenus


@router.post("/", response_model=Submenu, status_code=HTTPStatus.CREATED)
def submenu_create(menu_id: UUID, submenu: Submenu, session: Session = ActiveSession):
    menu = get_object_or_404(
        get_menu_by_id_query(menu_id),
        session,
        MENU_NOT_FOUND_MESSAGE,
    )
    menu.submenus.append(submenu)
    session.add(submenu)
    session.commit()
    session.refresh(submenu)
    return submenu


@router.patch("/{submenu_id}/")
def submenu_patch(
    menu_id: UUID,
    submenu_id: UUID,
    updated_submenu: Menu,
    session: Session = ActiveSession,
):
    query = get_submenu_query(menu_id, submenu_id)
    submenu = get_object_or_404(query, session, SUBMENU_NOT_FOUND_MESSAGE)

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


@router.delete("/{submenu_id}/")
def submenu_delete(menu_id: UUID, submenu_id: UUID, session: Session = ActiveSession):
    query = get_submenu_query(menu_id, submenu_id)
    submenu = get_object_or_404(query, session, SUBMENU_NOT_FOUND_MESSAGE)

    session.delete(submenu)
    session.commit()
    return {"status": True, "message": "The submenu has been deleted"}
