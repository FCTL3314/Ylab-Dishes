from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, select as sql_model_select
from sqlalchemy import func, distinct, select

from app.config import Config
from app.dish.schemas import DishBase
from app.menu.schemas import MenuBase
from app.submenu.schemas import SubmenuBase


class Menu(MenuBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)

    submenus: list["Submenu"] = Relationship(
        sa_relationship_kwargs={"cascade": "delete"}, back_populates="menu"
    )

    @classmethod
    def query_with_count(cls):
        return (
            select(
                cls.id,
                cls.title,
                cls.description,
                func.count(distinct(Submenu.id)).label("submenus_count"),
                func.count(distinct(Dish.id)).label("dishes_count"),
            )
            .outerjoin(Submenu, Submenu.menu_id == cls.id)
            .outerjoin(Dish, Dish.submenu_id == Submenu.id)
            .group_by(cls.id)
        )

    @classmethod
    def select_all(cls):
        return sql_model_select(cls)

    @classmethod
    def select_by_id(cls, identifier):
        return cls.select_all().where(cls.id == identifier)


class Submenu(SubmenuBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    menu_id: Optional[UUID] = Field(default=None, foreign_key="menu.id")

    menu: "Menu" = Relationship(back_populates="submenus")
    dishes: list["Dish"] = Relationship(
        sa_relationship_kwargs={"cascade": "delete"}, back_populates="submenu"
    )

    @classmethod
    def query_with_count(cls, menu_id):
        return (
            select(
                cls.id,
                cls.title,
                cls.description,
                func.count(distinct(Dish.id)).label("dishes_count"),
            )
            .outerjoin(Menu, Submenu.menu_id == Menu.id)
            .outerjoin(Dish, Dish.submenu_id == cls.id)
            .where(Menu.id == menu_id)
            .group_by(cls.id)
        )

    @classmethod
    def select_all(cls, menu_id):
        return sql_model_select(cls).where(cls.menu_id == menu_id)

    @classmethod
    def select_by_id(cls, menu_id, identifier):
        return cls.select_all(menu_id).where(cls.id == identifier)


class Dish(DishBase, table=True):
    def __init__(self, **kwargs):
        """Rounds price to dish rounding config setting."""
        if "price" in kwargs:
            template = f"{{:.{Config.DISH_PRICE_ROUNDING}f}}"
            kwargs["price"] = template.format(float(kwargs["price"]))
        super().__init__(**kwargs)

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    submenu_id: Optional[UUID] = Field(default=None, foreign_key="submenu.id")

    submenu: Submenu = Relationship(back_populates="dishes")

    @classmethod
    def select_all(cls, menu_id, submenu_id):
        return (
            sql_model_select(cls)
            .join(Submenu, cls.submenu_id == Submenu.id)
            .where(cls.submenu_id == submenu_id, Submenu.menu_id == menu_id)
        )

    @classmethod
    def select_by_id(cls, menu_id, submenu_id, identifier):
        return cls.select_all(menu_id, submenu_id).where(cls.id == identifier)
