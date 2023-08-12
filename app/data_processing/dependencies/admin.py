from dependencies import Injector

from app.data_processing.services.admin.admin_service import AdminService
from app.data_processing.services.admin.updating_services import (
    AdminDishService,
    AdminMenuService,
    AdminSubmenuService,
)
from app.dish.repository import DishRepository
from app.menu.repository import MenuRepository
from app.submenu.repository import SubmenuRepository


class AdminDependencies(Injector):
    admin_service = AdminService
    updating_services = [
        AdminMenuService[MenuRepository](MenuRepository()),
        AdminSubmenuService[SubmenuRepository](SubmenuRepository()),
        AdminDishService[DishRepository](DishRepository()),
    ]
