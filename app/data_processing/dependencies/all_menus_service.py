from fastapi import Depends

from app.data_processing.services.all_menus import (
    AllMenusService,
    CachedAllMenusService,
)


def all_menus_service() -> AllMenusService:
    return AllMenusService()


ActiveAllMenusService = Depends(all_menus_service)


def cached_all_menus_service() -> CachedAllMenusService:
    return CachedAllMenusService()


ActiveCachedAllMenusService = Depends(cached_all_menus_service)
