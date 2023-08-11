from fastapi import Depends

from app.menu.repository import MenuRepository, MenuWithCountingRepository
from app.menu.schemas import MenuBase, MenuNestedResponse, MenuResponse
from app.menu.services import CachedMenuService, MenuService


def menu_service() -> MenuService[MenuBase]:
    return MenuService[MenuBase](MenuRepository())


ActiveMenuService = Depends(menu_service)


def menu_nested_service() -> MenuService[MenuNestedResponse]:
    return MenuService[MenuNestedResponse](MenuRepository())


ActiveMenuNestedService = Depends(menu_service)


def menu_with_counting_service() -> MenuService[MenuResponse]:
    return MenuService[MenuResponse](MenuWithCountingRepository())


ActiveMenuWithCountingService = Depends(menu_with_counting_service)


def cached_menu_service() -> CachedMenuService[MenuResponse]:
    return CachedMenuService[MenuResponse](MenuWithCountingRepository())


ActiveCachedMenuService = Depends(cached_menu_service)
