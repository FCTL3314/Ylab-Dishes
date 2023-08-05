from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.schemas import DeletionResponse
from app.dependencies import ActiveCachedDishService, ActiveSession
from app.dish.services import CachedDishService
from app.models import Dish

router = APIRouter()


@router.get('/{dish_id}/', name='dish:retrieve', response_model=Dish)
async def dish_retrieve(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish_service: CachedDishService = ActiveCachedDishService,
    session: AsyncSession = ActiveSession,
) -> Dish:
    response = await dish_service.retrieve(menu_id, submenu_id, dish_id, session)
    return response


@router.get('/', name='dish:list', response_model=list[Dish])
async def dish_list(
    menu_id: UUID,
    submenu_id: UUID,
    dish_service: CachedDishService = ActiveCachedDishService,
    session: AsyncSession = ActiveSession,
) -> list[Dish]:
    response = await dish_service.list(menu_id, submenu_id, session)
    return response


@router.post('/', name='dish:create', response_model=Dish, status_code=HTTPStatus.CREATED)
async def dish_create(
    menu_id: UUID,
    submenu_id: UUID,
    dish: Dish,
    dish_service: CachedDishService = ActiveCachedDishService,
    session: AsyncSession = ActiveSession,
) -> Dish:
    response = await dish_service.create(menu_id, submenu_id, dish, session)
    return response


@router.patch('/{dish_id}/', name='dish:update', response_model=Dish)
async def dish_patch(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    updated_dish: Dish,
    dish_service: CachedDishService = ActiveCachedDishService,
    session: AsyncSession = ActiveSession,
) -> Dish:
    response = await dish_service.update(
        menu_id, submenu_id, dish_id, updated_dish, session
    )
    return response


@router.delete('/{dish_id}/', name='dish:delete', response_model=DeletionResponse)
async def dish_delete(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish_service: CachedDishService = ActiveCachedDishService,
    session: AsyncSession = ActiveSession,
) -> DeletionResponse:
    response = await dish_service.delete(menu_id, submenu_id, dish_id, session)
    return response
