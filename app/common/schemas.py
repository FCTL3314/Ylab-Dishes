from sqlmodel import SQLModel


class DeletionResponse(SQLModel):
    status: bool
    message: str
