from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dependencies import ActiveSession
from app.common.services import AbstractListService
from app.data_processing.constants import DATA_PROCESSING_TAG
from app.data_processing.dependencies.all_menus_service import (
    ActiveCachedAllMenusService,
)
from app.menu.schemas import MenuNestedResponse

router = APIRouter()


@router.get(
    '/all-menus',
    name='all-menus:list',
    tags=[DATA_PROCESSING_TAG],
    response_model=list[MenuNestedResponse],
)
async def all_menus_list(
        session: AsyncSession = ActiveSession,
        all_menus_service: AbstractListService = ActiveCachedAllMenusService,
) -> list[MenuNestedResponse]:
    return await all_menus_service.list(session)
