from dependencies import Injector
from fastapi import Depends

from app.data_processing.services.admin.admin_service import AdminFileService
from app.data_processing.services.admin.updating_services import (
    AdminDishUpdatingService,
    AdminMenuUpdatingService,
    AdminSubmenuUpdatingService,
)
from app.data_processing.services.all_menus import AllMenusService
from app.data_processing.tasks import all_menus_task
from app.dish.repository import DishRepository
from app.menu.repository import MenuRepository
from app.menu.schemas import MenuNestedResponse
from app.submenu.repository import SubmenuRepository


def all_menus_service() -> AllMenusService[MenuNestedResponse]:
    return AllMenusService[MenuNestedResponse](all_menus_task)


ActiveAllMenusService = Depends(all_menus_service)


class AdminFileDependencies(Injector):
    admin_file_service = AdminFileService
    updating_services = [
        AdminMenuUpdatingService[MenuRepository](MenuRepository()),
        AdminSubmenuUpdatingService[SubmenuRepository](SubmenuRepository()),
        AdminDishUpdatingService[DishRepository](DishRepository()),
    ]
