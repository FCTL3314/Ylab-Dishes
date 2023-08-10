from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.data_processing.constraints import DATA_PROCESSING_TAG
from app.dependencies import ActiveMenuService, ActiveSession
from app.menu.schemas import MenuNestedResponse
from app.menu.services import MenuService

router = APIRouter()


@router.get('/all/', tags=[DATA_PROCESSING_TAG], response_model=list[MenuNestedResponse])
async def all_data_retrieve(
        menu_service: MenuService = ActiveMenuService,
        session: AsyncSession = ActiveSession,
):
    return await menu_service.scalar_list(session)
