import pickle

from app.celery import celery
from app.data_processing.dependencies.admin import AdminDependencies
from app.db import scoped_loop, scoped_session
from app.menu.dependencies import menu_nested_service
from app.menu.schemas import MenuNestedResponse


async def all_menus_service() -> list[MenuNestedResponse]:
    """
    Gets all menu objects with nested submenus and dishes.
    """
    async with scoped_session() as session:
        return await menu_nested_service().list(session, scalar=True)


@celery.task()
def all_menus_task():
    """
    Runs all_menus_service function as a background task.
    """
    result = scoped_loop.run_until_complete(all_menus_service())
    return pickle.dumps(result)


async def database_synchronization_service() -> None:
    """
    Runs the service of synchronizing the database with the admin file.
    """
    async with scoped_session() as session:
        await AdminDependencies.admin_service.handle(session)  # type: ignore


@celery.task
def database_synchronization():
    """
    Runs database_synchronization_service function as a background task.
    """
    scoped_loop.run_until_complete(database_synchronization_service())
