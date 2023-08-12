from fastapi import Depends

from app.data_processing.services.all_menus import AllMenusService
from app.data_processing.tasks import all_menus_task
from app.menu.schemas import MenuNestedResponse


def all_menus_service() -> AllMenusService[MenuNestedResponse]:
    return AllMenusService[MenuNestedResponse](all_menus_task)


ActiveAllMenusService = Depends(all_menus_service)
