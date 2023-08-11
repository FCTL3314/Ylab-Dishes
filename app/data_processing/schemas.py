from sqlmodel import SQLModel


class TaskCreated(SQLModel):
    task_id: str
