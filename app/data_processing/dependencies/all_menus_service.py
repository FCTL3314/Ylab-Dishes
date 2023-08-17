from fastapi import Depends

from app.data_processing.services.all_menus import AllMenusService


def all_menus_service() -> AllMenusService:
    return AllMenusService()


ActiveAllMenusService = Depends(all_menus_service)
