from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dependencies import ActiveSession
from app.common.schemas import DeletionResponse
from app.models import Submenu
from app.submenu.constants import SUBMENU_TAG
from app.submenu.dependencies import ActiveCachedSubmenuService
from app.submenu.schemas import SubmenuResponse
from app.submenu.services import CachedSubmenuService

router = APIRouter()


@router.get(
    '/{submenu_id}/',
    name='submenu:retrieve',
    response_model=SubmenuResponse,
    description='Get submenu details by ID.',
    tags=[SUBMENU_TAG],
)
async def submenu_retrieve(
    menu_id: UUID,
    submenu_id: UUID,
    submenu_service: CachedSubmenuService = ActiveCachedSubmenuService,
    session: AsyncSession = ActiveSession,
) -> SubmenuResponse:
    response = await submenu_service.retrieve(menu_id, submenu_id, session)
    return response


@router.get(
    '/',
    name='submenu:list',
    response_model=list[SubmenuResponse],
    description='Get a list of all submenus.',
    tags=[SUBMENU_TAG],
)
async def submenu_list(
    menu_id: UUID,
    submenu_service: CachedSubmenuService = ActiveCachedSubmenuService,
    session: AsyncSession = ActiveSession,
) -> list[SubmenuResponse]:
    response = await submenu_service.list(menu_id, session)
    return response


@router.post(
    '/',
    name='submenu:create',
    response_model=SubmenuResponse,
    description='Create a new submenu.',
    status_code=HTTPStatus.CREATED,
    tags=[SUBMENU_TAG],
)
async def submenu_create(
    menu_id: UUID,
    submenu: Submenu,
    submenu_service: CachedSubmenuService = ActiveCachedSubmenuService,
    session: AsyncSession = ActiveSession,
) -> SubmenuResponse:
    response = await submenu_service.create(menu_id, submenu, session)
    return response


@router.patch(
    '/{submenu_id}/',
    name='submenu:update',
    response_model=SubmenuResponse,
    description='Update a submenu by ID.',
    tags=[SUBMENU_TAG],
)
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


@router.delete(
    '/{submenu_id}/',
    name='submenu:delete',
    response_model=DeletionResponse,
    description='Delete a submenu by ID.',
    tags=[SUBMENU_TAG],
)
async def submenu_delete(
    menu_id: UUID,
    submenu_id: UUID,
    submenu_service: CachedSubmenuService = ActiveCachedSubmenuService,
    session: AsyncSession = ActiveSession,
) -> DeletionResponse:
    response = await submenu_service.delete(menu_id, submenu_id, session)
    return response
