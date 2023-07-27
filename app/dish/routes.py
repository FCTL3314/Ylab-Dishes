from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter

from app.dish.repository import DishRepository
from app.models import Dish

router = APIRouter()


dish_repository = DishRepository()


@router.get("/{dish_id}/", response_model=Dish)
async def dish_retrieve(menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    return dish_repository.retrieve(menu_id, submenu_id, dish_id)


@router.get("/", response_model=list[Dish])
async def dish_list(menu_id: UUID, submenu_id: UUID):
    return dish_repository.list(menu_id, submenu_id)


@router.post("/", response_model=Dish, status_code=HTTPStatus.CREATED)
async def dish_create(menu_id: UUID, submenu_id: UUID, dish: Dish):
    return dish_repository.create(menu_id, submenu_id, dish)


@router.patch("/{dish_id}/", response_model=Dish)
async def dish_patch(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    updated_dish: Dish,
):
    return dish_repository.update(menu_id, submenu_id, dish_id, updated_dish)


@router.delete("/{dish_id}/")
async def dish_delete(menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    return dish_repository.delete(menu_id, submenu_id, dish_id)
