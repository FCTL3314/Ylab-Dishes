from fastapi import FastAPI
from sqlmodel import Session

from app.db import ActiveSession
from app.dish.models import Menu, Submenu, SubmenuWithNestedModels

app = FastAPI()


@app.get("/ping", response_model=SubmenuWithNestedModels)
def index(session: Session = ActiveSession):
    menu = Menu(name="Test")
    session.add(menu)
    session.commit()
    submenu = Submenu(name="TestSubMenu", menu_id=menu.id)
    session.add(submenu)
    session.commit()
    return submenu
