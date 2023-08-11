import pickle

from app.celery import celery
from app.db import scoped_loop, scoped_session
from app.dependencies import menu_nested_service
from app.menu.schemas import MenuNestedResponse


async def all_data_report_process() -> list[MenuNestedResponse]:
    async with scoped_session() as session:
        return await menu_nested_service().list(session, scalar=True)


@celery.task()
def all_data_report_process_task():
    result = scoped_loop.run_until_complete(all_data_report_process())
    return pickle.dumps(result)
