from sqlalchemy.ext.asyncio import AsyncSession

from app.data_processing.services.admin.admin_update_services import (
    BaseAdminUpdateService,
)


class AdminService:
    """
    Accepts services for synchronizing specific models
    with the admin file, and executes them.
    """

    def __init__(self, update_services: list[BaseAdminUpdateService]):
        self.update_services = update_services

    async def handle(self, session: AsyncSession):
        """
        Iterate through the provided update services and perform synchronization
        between database models and admin file.
        """
        for update_service in self.update_services:
            await update_service.update(session)
