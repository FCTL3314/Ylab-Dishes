from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from sqlmodel import Session, select

from app.dependencies import ActiveSession
from app.models import Menu, MenuResponse
from app.utils import get_object_or_404

router = APIRouter()

MENU_NOT_FOUND_MESSAGE = "menu not found"


def get_menu_by_id_query(menu_id):
    return select(Menu).where(Menu.id == menu_id)


@router.get("/{menu_id}/", response_model=MenuResponse)
async def menu_retrieve(menu_id: UUID, session: Session = ActiveSession):
    menu = get_object_or_404(
        get_menu_by_id_query(menu_id), session, MENU_NOT_FOUND_MESSAGE
    )
    return {
        **menu.dict(),
        "submenus_count": menu.submenus_count,
        "dishes_count": menu.dishes_count,
    }


@router.get("/", response_model=list[MenuResponse])
async def menu_list(session: Session = ActiveSession):
    query = select(Menu)
    menus = session.exec(query).all()
    return [
        {
            **menu.dict(),
            "submenus_count": menu.submenus_count,
            "dishes_count": menu.dishes_count,
        }
        for menu in menus
    ]


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
    menu = get_object_or_404(
        get_menu_by_id_query(menu_id), session, MENU_NOT_FOUND_MESSAGE
    )

    updated_menu_dict = updated_menu.dict(exclude_unset=True)
    for key, val in updated_menu_dict.items():
        setattr(menu, key, val)

    session.add(menu)
    session.commit()
    session.refresh(menu)
    return {
        **menu.dict(),
        "submenus_count": menu.submenus_count,
        "dishes_count": menu.dishes_count,
    }


@router.delete("/{menu_id}/")
async def menu_delete(menu_id: UUID, session: Session = ActiveSession):
    menu = get_object_or_404(
        get_menu_by_id_query(menu_id), session, MENU_NOT_FOUND_MESSAGE
    )
    session.delete(menu)
    session.commit()
    return {"status": True, "message": "The menu has been deleted"}
