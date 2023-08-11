from sqlmodel import SQLModel


class AllDataReportTaskCreated(SQLModel):
    task_id: str
