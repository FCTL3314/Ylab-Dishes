from app.celery import celery
from app.data_processing.dependencies.admin import AdminDependencies
from app.db import scoped_loop, scoped_session


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
