from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from sqlmodel import Session

from app.dependencies import ActiveSession
from app.dish.services import DishService
from app.models import Dish

router = APIRouter()


@router.get("/{dish_id}/", response_model=Dish)
async def dish_retrieve(
    menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: Session = ActiveSession
):
    return DishService.retrieve(menu_id, submenu_id, dish_id, session)


@router.get("/", response_model=list[Dish])
async def dish_list(menu_id: UUID, submenu_id: UUID, session: Session = ActiveSession):
    return DishService.list(menu_id, submenu_id, session)


@router.post("/", response_model=Dish, status_code=HTTPStatus.CREATED)
async def dish_create(
    menu_id: UUID, submenu_id: UUID, dish: Dish, session: Session = ActiveSession
):
    return DishService.create(menu_id, submenu_id, dish, session)


@router.patch("/{dish_id}/", response_model=Dish)
async def dish_patch(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    updated_dish: Dish,
    session: Session = ActiveSession,
):
    return DishService.update(menu_id, submenu_id, dish_id, updated_dish, session)


@router.delete("/{dish_id}/")
async def dish_delete(
    menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: Session = ActiveSession
):
    return DishService.delete(menu_id, submenu_id, dish_id, session)
