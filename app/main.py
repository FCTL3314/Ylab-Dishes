from fastapi import FastAPI, APIRouter

from app.dish.routes import router as dish_router

app = FastAPI()
router = APIRouter(prefix="/api/v1")


@router.get("/ping")
def ping():
    return {"msg": "pong"}


router.include_router(dish_router)
app.include_router(router)
