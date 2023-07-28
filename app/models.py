from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from app.config import Config
from app.dish.schemas import DishBase
from app.menu.schemas import MenuBase
from app.submenu.schemas import SubmenuBase


class Menu(MenuBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)

    submenus: list["Submenu"] = Relationship(
        sa_relationship_kwargs={"cascade": "delete"}, back_populates="menu"
    )


class Submenu(SubmenuBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    menu_id: Optional[UUID] = Field(default=None, foreign_key="menu.id")

    menu: "Menu" = Relationship(back_populates="submenus")
    dishes: list["Dish"] = Relationship(
        sa_relationship_kwargs={"cascade": "delete"}, back_populates="submenu"
    )


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
