from uuid import UUID

from sqlmodel import SQLModel


class MenuBase(SQLModel):
    id: UUID
    title: str
    description: str


class MenuResponse(MenuBase):
    submenus_count: int
    dishes_count: int
