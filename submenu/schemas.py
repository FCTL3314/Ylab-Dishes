from uuid import UUID

from sqlmodel import SQLModel


class SubmenuBase(SQLModel):
    id: UUID
    title: str
    description: str


class SubmenuResponse(SubmenuBase):
    dishes_count: int
