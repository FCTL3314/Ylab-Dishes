from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from sqlmodel import Session, select

from app.dependencies import ActiveSession
from app.models import Dish, Submenu
from app.submenu.routes import SUBMENU_NOT_FOUND_MESSAGE, get_submenu_by_id
from app.utils import get_first_or_404

router = APIRouter()

DISH_NOT_FOUND_MESSAGE = "dish not found"


def get_dishes_query(menu_id, submenu_id):
    return (
        select(Dish)
        .join(Submenu, Dish.submenu_id == Submenu.id)
        .where(Dish.submenu_id == submenu_id, Submenu.menu_id == menu_id)
    )


def get_dish_by_id(menu_id, submenu_id, dish_id):
    return get_dishes_query(menu_id, submenu_id).where(Dish.id == dish_id)


@router.get("/{dish_id}/", response_model=Dish)
async def dish_retrieve(
    menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: Session = ActiveSession
):
    dish = get_first_or_404(
        get_dish_by_id(menu_id, submenu_id, dish_id),
        session,
        DISH_NOT_FOUND_MESSAGE,
    )
    return dish


@router.get("/", response_model=list[Dish])
async def dish_list(menu_id: UUID, submenu_id: UUID, session: Session = ActiveSession):
    return session.exec(get_dishes_query(menu_id, submenu_id)).all()


@router.post("/", response_model=Dish, status_code=HTTPStatus.CREATED)
async def dish_create(
    menu_id: UUID, submenu_id: UUID, dish: Dish, session: Session = ActiveSession
):
    submenu = get_first_or_404(
        get_submenu_by_id(menu_id, submenu_id),
        session,
        SUBMENU_NOT_FOUND_MESSAGE,
    )
    submenu.dishes.append(dish)
    session.add(dish)
    session.commit()
    session.refresh(dish)
    return dish


@router.patch("/{dish_id}/", response_model=Dish)
async def dish_patch(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    updated_dish: Dish,
    session: Session = ActiveSession,
):
    dish = get_first_or_404(
        get_dish_by_id(menu_id, submenu_id, dish_id),
        session,
        DISH_NOT_FOUND_MESSAGE,
    )

    updated_dish_dict = updated_dish.dict(exclude_unset=True)

    for key, val in updated_dish_dict.items():
        setattr(dish, key, val)

    session.add(dish)
    session.commit()
    session.refresh(dish)
    return dish


@router.delete("/{dish_id}/")
async def dish_delete(
    menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: Session = ActiveSession
):
    dish = get_first_or_404(
        get_dish_by_id(menu_id, submenu_id, dish_id),
        session,
        DISH_NOT_FOUND_MESSAGE,
    )

    session.delete(dish)
    session.commit()
    return {"status": True, "message": "The dish has been deleted"}
