from sqlmodel import Field, Relationship, SQLModel


class MenuBase(SQLModel):
    id: int
    name: str


class Menu(MenuBase, table=True):
    id: int = Field(primary_key=True)
    name: str
    description: str

    submenus: list["Submenu"] = Relationship(back_populates="menu")


class MenuWithNestedModels(MenuBase):
    submenus: list["MenuBase"] = []


class SubmenuBase(SQLModel):
    id: int
    name: str


class Submenu(SubmenuBase, table=True):
    id: int = Field(primary_key=True)
    name: str
    menu_id: int = Field(foreign_key="menu.id")

    menu: Menu = Relationship(back_populates="submenus")


class SubmenuWithNestedModels(SubmenuBase):
    menu: Menu
