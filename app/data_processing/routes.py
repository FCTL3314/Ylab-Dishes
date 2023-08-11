import pickle
from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from app.celery import celery
from app.data_processing.constraints import DATA_PROCESSING_TAG
from app.data_processing.schemas import AllDataReportTaskCreated
from app.data_processing.tasks import all_data_report_process_task
from app.menu.schemas import MenuNestedResponse

router = APIRouter()


@router.get(
    '/all/{task_id}/',
    tags=[DATA_PROCESSING_TAG],
    response_model=list[MenuNestedResponse],
)
async def all_data_report_retrieve(task_id: str) -> list[MenuNestedResponse]:
    task = celery.AsyncResult(task_id)
    if task.ready():
        return pickle.loads(task.result)
    raise HTTPException(
        detail='Task not found or still being processing.',
        status_code=HTTPStatus.ACCEPTED,
    )


@router.post(
    '/all/',
    tags=[DATA_PROCESSING_TAG],
    status_code=HTTPStatus.CREATED,
)
async def all_data_report_create() -> AllDataReportTaskCreated:
    task = all_data_report_process_task.delay()
    return AllDataReportTaskCreated(task_id=task.id)
