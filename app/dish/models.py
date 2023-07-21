from sqlmodel import SQLModel, Field, Relationship


class MenuBase(SQLModel):
    id: int
    name: str


class Menu(MenuBase, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str

    submenus: list["Submenu"] = Relationship(back_populates="menu")


class MenuWithNestedModels(MenuBase):
    submenus: list["MenuBase"] = []


class SubmenuBase(SQLModel):
    id: int
    name: str


class Submenu(SubmenuBase, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    menu_id: int = Field(default=None, foreign_key="menu.id")

    menu: Menu = Relationship(back_populates="submenus")


class SubmenuWithNestedModels(SubmenuBase):
    menu: Menu
