import pickle

from app.celery import celery
from app.db import scoped_loop, scoped_session
from app.dependencies import menu_service


async def all_data_report_process():
    async with scoped_session() as session:
        service = menu_service()
        result = await service.scalar_list(session)
        return result


@celery.task()
def all_data_report_process_task():
    result = scoped_loop.run_until_complete(all_data_report_process())
    return pickle.dumps(result)
