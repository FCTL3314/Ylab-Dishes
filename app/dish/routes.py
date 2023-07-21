from fastapi import APIRouter
from sqlmodel import Session, select
from http import HTTPStatus

from app.db import ActiveSession
from app.dish.models import Menu, MenuBase

router = APIRouter()


@router.get("/menus", response_model=list[Menu])
def menu_list(session: Session = ActiveSession):
    statement = select(Menu)
    menus = session.exec(statement).all()
    return menus


@router.post("/menus", response_model=Menu, status_code=HTTPStatus.CREATED)
def create_menu(menu: Menu, session: Session = ActiveSession):
    session.add(menu)
    session.commit()
    session.refresh(menu)
    return menu
