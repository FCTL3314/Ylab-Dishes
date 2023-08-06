from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.schemas import DeletionResponse
from app.dependencies import ActiveCachedMenuService, ActiveSession
from app.menu.constants import MENU_TAG
from app.menu.schemas import MenuResponse
from app.menu.services import CachedMenuService
from app.models import Menu

router = APIRouter()


@router.get(
    '/{menu_id}/',
    name='menu:retrieve',
    response_model=MenuResponse,
    description='Get menu details by ID.',
    tags=[MENU_TAG],
)
async def menu_retrieve(
    menu_id: UUID,
    menu_service: CachedMenuService = ActiveCachedMenuService,
    session: AsyncSession = ActiveSession,
) -> MenuResponse:
    response = await menu_service.retrieve(menu_id, session)
    return response


@router.get(
    '/',
    name='menu:list',
    response_model=list[MenuResponse],
    description='Get a list of all menus.',
    tags=[MENU_TAG],
)
async def menu_list(
    menu_service: CachedMenuService = ActiveCachedMenuService,
    session: AsyncSession = ActiveSession,
) -> list[MenuResponse]:
    response = await menu_service.list(session)
    return response


@router.post(
    '/',
    response_model=MenuResponse,
    name='menu:create',
    description='Create a new menu.',
    status_code=HTTPStatus.CREATED,
    tags=[MENU_TAG],
)
async def menu_create(
    menu: Menu,
    menu_service: CachedMenuService = ActiveCachedMenuService,
    session: AsyncSession = ActiveSession,
) -> MenuResponse:
    response = await menu_service.create(menu, session)
    return response


@router.patch(
    '/{menu_id}/',
    name='menu:update',
    response_model=MenuResponse,
    description='Update a menu by ID.',
    tags=[MENU_TAG],
)
async def menu_patch(
    menu_id: UUID,
    updated_menu: Menu,
    menu_service: CachedMenuService = ActiveCachedMenuService,
    session: AsyncSession = ActiveSession,
) -> MenuResponse:
    response = await menu_service.update(menu_id, updated_menu, session)
    return response


@router.delete(
    '/{menu_id}/',
    name='menu:delete',
    response_model=DeletionResponse,
    description='Delete a menu by ID.',
    tags=[MENU_TAG],
)
async def menu_delete(
    menu_id: UUID,
    menu_service: CachedMenuService = ActiveCachedMenuService,
    session: AsyncSession = ActiveSession,
) -> DeletionResponse:
    response = await menu_service.delete(menu_id, session)
    return response
