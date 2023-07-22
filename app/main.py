from fastapi import FastAPI, APIRouter

from app.menu.routes import router as menu_router
from app.submenu.routes import router as submenu_router
from app.dish.routes import router as dish_router

app = FastAPI()
router = APIRouter(prefix="/api/v1")


@router.get("/ping")
def ping():
    return {"msg": "pong"}


submenu_router.include_router(dish_router, prefix="/{submenu_id}/dishes")
menu_router.include_router(submenu_router, prefix="/{menu_id}/submenus")
router.include_router(menu_router, prefix="/menus")
app.include_router(router)
