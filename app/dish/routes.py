from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dependencies import ActiveSession
from app.common.schemas import DeletionResponse
from app.dish.constants import DISH_TAG
from app.dish.dependencies import ActiveCachedDishService
from app.dish.services import CachedDishService
from app.models import Dish

router = APIRouter()


@router.get(
    '/{dish_id}/',
    name='dish:retrieve',
    response_model=Dish,
    description='Get dish details by ID.',
    tags=[DISH_TAG],
)
async def dish_retrieve(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish_service: CachedDishService = ActiveCachedDishService,
    session: AsyncSession = ActiveSession,
) -> Dish:
    response = await dish_service.retrieve(menu_id, submenu_id, dish_id, session, scalar=True)
    return response


@router.get(
    '/', name='dish:list',
    response_model=list[Dish],
    description='Get a list of all dishes.',
    tags=[DISH_TAG],
)
async def dish_list(
    menu_id: UUID,
    submenu_id: UUID,
    dish_service: CachedDishService = ActiveCachedDishService,
    session: AsyncSession = ActiveSession,
) -> list[Dish]:
    response = await dish_service.list(menu_id, submenu_id, session, scalar=True)
    return response


@router.post(
    '/',
    name='dish:create',
    response_model=Dish,
    description='Create a new dish.',
    status_code=HTTPStatus.CREATED,
    tags=[DISH_TAG],
)
async def dish_create(
    menu_id: UUID,
    submenu_id: UUID,
    dish: Dish,
    dish_service: CachedDishService = ActiveCachedDishService,
    session: AsyncSession = ActiveSession,
) -> Dish:
    response = await dish_service.create(menu_id, submenu_id, dish, session)
    return response


@router.patch(
    '/{dish_id}/',
    name='dish:update',
    response_model=Dish,
    description='Update a dish by ID.',
    tags=[DISH_TAG],
)
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


@router.delete(
    '/{dish_id}/',
    name='dish:delete',
    response_model=DeletionResponse,
    description='Delete a dish by ID.',
    tags=[DISH_TAG],
)
async def dish_delete(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish_service: CachedDishService = ActiveCachedDishService,
    session: AsyncSession = ActiveSession,
) -> DeletionResponse:
    response = await dish_service.delete(menu_id, submenu_id, dish_id, session)
    return response
