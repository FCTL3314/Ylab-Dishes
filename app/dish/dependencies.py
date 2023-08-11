from fastapi import Depends

from app.dish.repository import DishRepository
from app.dish.schemas import DishBase
from app.dish.services import CachedDishService, DishService


def dish_service() -> DishService[DishBase]:
    return DishService[DishBase](DishRepository())


ActiveDishService = Depends(dish_service)


def cached_dish_service() -> CachedDishService[DishBase]:
    return CachedDishService[DishBase](DishRepository())


ActiveCachedDishService = Depends(cached_dish_service)
