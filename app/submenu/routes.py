from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.schemas import DeletionResponse
from app.dependencies import ActiveCachedSubmenuService, ActiveSession
from app.models import Submenu
from app.submenu.schemas import SubmenuResponse
from app.submenu.services import CachedSubmenuService

router = APIRouter()


@router.get('/{submenu_id}/', response_model=SubmenuResponse)
async def submenu_retrieve(
    menu_id: UUID,
    submenu_id: UUID,
    submenu_service: CachedSubmenuService = ActiveCachedSubmenuService,
    session: AsyncSession = ActiveSession,
) -> SubmenuResponse:
    response = await submenu_service.retrieve(menu_id, submenu_id, session)
    return response


@router.get('/', response_model=list[SubmenuResponse])
async def submenu_list(
    menu_id: UUID,
    submenu_service: CachedSubmenuService = ActiveCachedSubmenuService,
    session: AsyncSession = ActiveSession,
) -> list[SubmenuResponse]:
    response = await submenu_service.list(menu_id, session)
    return response


@router.post('/', response_model=SubmenuResponse, status_code=HTTPStatus.CREATED)
async def submenu_create(
    menu_id: UUID,
    submenu: Submenu,
    submenu_service: CachedSubmenuService = ActiveCachedSubmenuService,
    session: AsyncSession = ActiveSession,
) -> SubmenuResponse:
    response = await submenu_service.create(menu_id, submenu, session)
    return response


@router.patch('/{submenu_id}/', response_model=SubmenuResponse)
async def submenu_patch(
    menu_id: UUID,
    submenu_id: UUID,
    updated_submenu: Submenu,
    submenu_service: CachedSubmenuService = ActiveCachedSubmenuService,
    session: AsyncSession = ActiveSession,
) -> SubmenuResponse:
    response = await submenu_service.update(
        menu_id, submenu_id, updated_submenu, session
    )
    return response


@router.delete('/{submenu_id}/')
async def submenu_delete(
    menu_id: UUID,
    submenu_id: UUID,
    submenu_service: CachedSubmenuService = ActiveCachedSubmenuService,
    session: AsyncSession = ActiveSession,
) -> DeletionResponse:
    response = await submenu_service.delete(menu_id, submenu_id, session)
    return response
