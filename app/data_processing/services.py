import pickle
from http import HTTPStatus
from typing import Generic, TypeVar

from fastapi import HTTPException

from app.celery import celery
from app.common.services import AbstractBackgroundService
from app.data_processing.schemas import TaskCreated

TASK_NOT_FOUND_MESSAGE = 'Task not found or still being processing.'


TaskResultType = TypeVar('TaskResultType')


class AllMenusService(AbstractBackgroundService, Generic[TaskResultType]):

    async def get_task_result(self, task_id: str) -> TaskResultType:
        task = celery.AsyncResult(task_id)
        if task.ready():
            return pickle.loads(task.result)
        raise HTTPException(
            detail=TASK_NOT_FOUND_MESSAGE,
            status_code=HTTPStatus.ACCEPTED,
        )

    async def create_task(self) -> TaskCreated:
        task = self.task_function.delay()
        return TaskCreated(task_id=task.id)
