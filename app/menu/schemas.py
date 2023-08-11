from uuid import UUID

from sqlmodel import SQLModel

from app.submenu.schemas import SubmenuNestedResponse


class MenuBase(SQLModel):
    id: UUID
    title: str
    description: str


class MenuResponse(MenuBase):
    submenus_count: int
    dishes_count: int


class MenuNestedResponse(MenuBase):
    submenus: list[SubmenuNestedResponse] = []
