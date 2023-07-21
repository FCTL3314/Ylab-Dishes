from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel


class MenuBase(SQLModel):
    id: UUID
    title: str
    description: str


class Menu(MenuBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)

    submenus: list["Submenu"] = Relationship(back_populates="menu")


class MenuWithNestedModels(MenuBase):
    submenus: list["MenuBase"] = []


class SubmenuBase(SQLModel):
    id: UUID
    title: str
    description: str


class Submenu(SubmenuBase, table=True):
    id: Optional[UUID] = Field(default=uuid4(), primary_key=True)
    menu_id: UUID = Field(foreign_key="menu.id")

    menu: Menu = Relationship(back_populates="submenus")


class SubmenuWithNestedModels(SubmenuBase):
    menu: Menu
