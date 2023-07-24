from uuid import UUID

from sqlmodel import SQLModel


class DishBase(SQLModel):
    id: UUID
    title: str
    description: str
    price: str
