from http import HTTPStatus

from fastapi import APIRouter

from app.data_processing.constraints import DATA_PROCESSING_TAG
from app.data_processing.dependencies.all_menus_service import ActiveAllMenusService
from app.data_processing.schemas import TaskCreated
from app.data_processing.services.all_menus import AllMenusService
from app.menu.schemas import MenuNestedResponse

router = APIRouter()


@router.get(
    '/all/{task_id}/',
    name='all-menus:list',
    tags=[DATA_PROCESSING_TAG],
    response_model=list[MenuNestedResponse],
)
async def all_menus_list(
        task_id: str,
        all_menus_service: AllMenusService = ActiveAllMenusService,
) -> list[MenuNestedResponse]:
    return await all_menus_service.get_task_result(task_id)


@router.post(
    '/all/',
    name='all-menus:create-task',
    tags=[DATA_PROCESSING_TAG],
    status_code=HTTPStatus.CREATED,
    response_model=TaskCreated,
)
async def all_menus_task_create(
        all_menus_service: AllMenusService = ActiveAllMenusService,
) -> TaskCreated:
    return await all_menus_service.create_task()
