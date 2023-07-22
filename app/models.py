from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from app.config import Config


class MenuBase(SQLModel):
    id: UUID
    title: str
    description: str


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


class MenuWithNestedModels(MenuBase):
    submenus: list["MenuBase"] = []


class SubmenuBase(SQLModel):
    id: UUID
    title: str
    description: str


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


class SubmenuWithNestedModels(SubmenuBase):
    menu: "Menu"
    dishes: list["DishBase"] = []


class DishBase(SQLModel):
    id: UUID
    title: str
    description: str
    price: str


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
