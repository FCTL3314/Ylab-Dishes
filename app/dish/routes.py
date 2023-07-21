from fastapi import APIRouter
from sqlmodel import Session, select

from app.db import ActiveSession
from app.dish.models import Menu

router = APIRouter()


@router.get("/menus", response_model=list[Menu])
def menu_list(session: Session = ActiveSession):
    query = select(Menu).limit(100)
    menus = session.exec(query).all()
    return menus
