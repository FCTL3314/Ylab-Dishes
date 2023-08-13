from dependencies import Injector

from app.data_processing.services.admin.admin_service import AdminService
from app.data_processing.services.admin.admin_update_services import (
    AdminDishUpdateService,
    AdminMenuUpdateService,
    AdminSubmenuUpdateService,
)
from app.dish.repository import DishRepository
from app.menu.repository import MenuRepository
from app.submenu.repository import SubmenuRepository


class AdminDependencies(Injector):
    admin_service = AdminService
    update_services = [
        AdminMenuUpdateService[MenuRepository](MenuRepository()),
        AdminSubmenuUpdateService[SubmenuRepository](SubmenuRepository()),
        AdminDishUpdateService[DishRepository](DishRepository()),
    ]
