from uuid import UUID

from sqlmodel import SQLModel

from app.dish.schemas import DishBase


class SubmenuBase(SQLModel):
    id: UUID
    title: str
    description: str


class SubmenuResponse(SubmenuBase):
    dishes_count: int


class SubmenuNestedResponse(SubmenuBase):
    dishes: list[DishBase] = []
