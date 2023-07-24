from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, select

from app.config import Config
from app.dish.schemas import DishBase
from app.menu.schemas import MenuBase
from submenu.schemas import SubmenuBase


class Menu(MenuBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)

    submenus: list["Submenu"] = Relationship(
        sa_relationship_kwargs={"cascade": "delete"}, back_populates="menu"
    )

    @property
    def submenus_count(self):
        return len(self.submenus)

    @property
    def dishes_count(self):
        return sum(submenu.dishes_count for submenu in self.submenus)

    @classmethod
    def select_all(cls):
        return select(cls)

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

    @property
    def dishes_count(self):
        return len(self.dishes)

    @classmethod
    def select_all(cls, menu_id):
        return select(cls).where(cls.menu_id == menu_id)

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
            select(cls)
            .join(Submenu, cls.submenu_id == Submenu.id)
            .where(cls.submenu_id == submenu_id, Submenu.menu_id == menu_id)
        )

    @classmethod
    def select_by_id(cls, menu_id, submenu_id, identifier):
        return cls.select_all(menu_id, submenu_id).where(cls.id == identifier)
