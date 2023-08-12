import pickle

from app.celery import celery
from app.data_processing.dependencies.admin import AdminDependencies
from app.db import scoped_loop, scoped_session
from app.menu.dependencies import menu_nested_service
from app.menu.schemas import MenuNestedResponse


async def get_all_menus() -> list[MenuNestedResponse]:
    async with scoped_session() as session:
        return await menu_nested_service().list(session, scalar=True)


@celery.task()
def all_menus_task():
    result = scoped_loop.run_until_complete(get_all_menus())
    return pickle.dumps(result)


async def database_synchronization_process() -> None:
    async with scoped_session() as session:
        await AdminDependencies.admin_service.handle(session)  # type: ignore


@celery.task
def database_synchronization():
    scoped_loop.run_until_complete(database_synchronization_process())
