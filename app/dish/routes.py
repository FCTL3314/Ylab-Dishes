from uuid import UUID

from fastapi import APIRouter
from sqlmodel import Session, select
from http import HTTPStatus

from app.db import ActiveSession
from app.models import Dish, Submenu, Menu
from app.submenu.routes import SUBMENU_NOT_FOUND_MESSAGE, get_submenu_query
from app.utils import get_object_or_404

router = APIRouter()

DISH_NOT_FOUND_MESSAGE = "dish not found"


@router.get('/{dish_id}/')
def dish_retrieve(menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: Session = ActiveSession):
    query = select(Dish).select_from(Menu).select_from(Submenu).where(
        Dish.id == dish_id,
        Submenu.id == submenu_id,
        Menu.id == menu_id,
    )
    dish = get_object_or_404(query, session, DISH_NOT_FOUND_MESSAGE)
    return dish


@router.get("/", response_model=list[Dish])
def dish_list(menu_id: UUID, submenu_id: UUID, session: Session = ActiveSession):
    query = select(Dish).select_from(Menu).select_from(Submenu).where(
        Submenu.id == submenu_id,
        Menu.id == menu_id,
    )
    return session.exec(query).all()


@router.post("/", response_model=Dish, status_code=HTTPStatus.CREATED)
def dish_create(menu_id: UUID, submenu_id: UUID, dish: Dish, session: Session = ActiveSession):
    query = get_submenu_query(menu_id, submenu_id)
    submenu = get_object_or_404(query, session, SUBMENU_NOT_FOUND_MESSAGE)
    submenu.dishes.append(dish)
    session.add(dish)
    session.commit()
    session.refresh(dish)
    return dish


@router.patch('/{dish_id}/')
def dish_patch(menu_id: UUID, submenu_id: UUID, dish_id: UUID, updated_dish: Dish, session: Session = ActiveSession):
    query = select(Dish).select_from(Menu).select_from(Submenu).where(
        Dish.id == dish_id,
        Submenu.id == submenu_id,
        Menu.id == menu_id,
    )
    dish = get_object_or_404(query, session, DISH_NOT_FOUND_MESSAGE)

    updated_dish_dict = updated_dish.dict(exclude_unset=True)

    for key, val in updated_dish_dict.items():
        setattr(dish, key, val)

    session.add(dish)
    session.commit()
    session.refresh(dish)
    return dish


@router.delete("/{dish_id}/")
def dish_delete(menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: Session = ActiveSession):
    query = select(Dish).select_from(Menu).select_from(Submenu).where(
        Dish.id == dish_id,
        Submenu.id == submenu_id,
        Menu.id == menu_id,
    )
    dish = get_object_or_404(query, session, DISH_NOT_FOUND_MESSAGE)

    session.delete(dish)
    session.commit()
    return {"status": True, "message": "The dish has been deleted"}
