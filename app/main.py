from fastapi import APIRouter, FastAPI

from app.config import Config
from app.data_processing.routes import router as data_processing_router
from app.dish.routes import router as dish_router
from app.menu.routes import router as menu_router
from app.submenu.routes import router as submenu_router

app = FastAPI(debug=Config.DEBUG)
router = APIRouter(prefix='/api/v1')


@router.get(
    '/ping',
    tags=['Utility'],
    description='Check if the server is running.',
)
async def ping():
    return {'msg': 'pong'}


submenu_router.include_router(dish_router, prefix='/{submenu_id}/dishes')
menu_router.include_router(submenu_router, prefix='/{menu_id}/submenus')
router.include_router(menu_router, prefix='/menus')
router.include_router(data_processing_router, prefix='/data-processing')
app.include_router(router)
