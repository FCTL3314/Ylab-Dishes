from http import HTTPStatus

from fastapi import APIRouter

from app.data_processing.constraints import DATA_PROCESSING_TAG
from app.data_processing.dependencies import ActiveAllMenusService
from app.data_processing.schemas import TaskCreated
from app.data_processing.services.admin_file import (
    AdminDishUpdatingService,
    AdminFileService,
    AdminMenuUpdatingService,
    AdminSubmenuUpdatingService,
)
from app.data_processing.services.all_menus import AllMenusService
from app.dish.repository import DishRepository
from app.menu.repository import MenuRepository
from app.menu.schemas import MenuNestedResponse
from app.submenu.repository import SubmenuRepository

router = APIRouter()


@router.get(
    '/all/{task_id}/',
    tags=[DATA_PROCESSING_TAG],
    response_model=list[MenuNestedResponse],
)
async def menus_with_attachments_list(
        task_id: str,
        all_menus_service: AllMenusService = ActiveAllMenusService,
) -> list[MenuNestedResponse]:
    return await all_menus_service.get_task_result(task_id)


@router.post(
    '/all/',
    tags=[DATA_PROCESSING_TAG],
    status_code=HTTPStatus.CREATED,
    response_model=TaskCreated,
)
async def menus_with_attachments_task_create(
        all_menus_service: AllMenusService = ActiveAllMenusService,
) -> TaskCreated:
    return await all_menus_service.create_task()


@router.get(
    '/test/',
    tags=[DATA_PROCESSING_TAG],
    status_code=HTTPStatus.CREATED,
)
async def test():
    return await AdminFileService(
        [
            AdminMenuUpdatingService[MenuRepository](MenuRepository()),
            AdminSubmenuUpdatingService[SubmenuRepository](SubmenuRepository()),
            AdminDishUpdatingService[DishRepository](DishRepository()),
        ]
    ).handle()
