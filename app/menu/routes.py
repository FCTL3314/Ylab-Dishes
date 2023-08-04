from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import ActiveCachedMenuService, ActiveSession
from app.menu.schemas import MenuResponse
from app.menu.services import CachedMenuService
from app.models import Menu

router = APIRouter()


@router.get('/{menu_id}/', response_model=MenuResponse)
async def menu_retrieve(
    menu_id: UUID,
    menu_service: CachedMenuService = ActiveCachedMenuService,
    session: AsyncSession = ActiveSession,
) -> MenuResponse:
    response = await menu_service.retrieve(menu_id, session)
    return response


@router.get('/', response_model=list[MenuResponse])
async def menu_list(
    menu_service: CachedMenuService = ActiveCachedMenuService,
    session: AsyncSession = ActiveSession,
) -> list[MenuResponse]:
    response = await menu_service.list(session)
    return response


@router.post('/', response_model=MenuResponse, status_code=HTTPStatus.CREATED)
async def menu_create(
    menu: Menu,
    menu_service: CachedMenuService = ActiveCachedMenuService,
    session: AsyncSession = ActiveSession,
) -> MenuResponse:
    response = await menu_service.create(menu, session)
    return response


@router.patch('/{menu_id}/', response_model=MenuResponse)
async def menu_patch(
    menu_id: UUID,
    updated_menu: Menu,
    menu_service: CachedMenuService = ActiveCachedMenuService,
    session: AsyncSession = ActiveSession,
) -> MenuResponse:
    response = await menu_service.update(menu_id, updated_menu, session)
    return response


@router.delete('/{menu_id}/')
async def menu_delete(
    menu_id: UUID,
    menu_service: CachedMenuService = ActiveCachedMenuService,
    session: AsyncSession = ActiveSession,
) -> dict:
    response = await menu_service.delete(menu_id, session)
    return response
