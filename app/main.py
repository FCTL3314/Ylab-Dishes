from fastapi import APIRouter, FastAPI

from app.config import Config
from app.dish.routes import router as dish_router
from app.menu.routes import router as menu_router
from app.submenu.routes import router as submenu_router

app = FastAPI(debug=Config.DEBUG)
router = APIRouter(prefix="/api/v1")


@router.get("/ping")
async def ping():
    return {"msg": "pong"}


submenu_router.include_router(dish_router, prefix="/{submenu_id}/dishes")
menu_router.include_router(submenu_router, prefix="/{menu_id}/submenus")
router.include_router(menu_router, prefix="/menus")
app.include_router(router)
