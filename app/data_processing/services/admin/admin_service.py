from sqlalchemy.ext.asyncio import AsyncSession

from app.data_processing.services.admin.admin_update_services import (
    BaseAdminUpdateService,
)


class AdminService:

    def __init__(self, update_services: list[BaseAdminUpdateService]):
        self.update_services = update_services

    async def handle(self, session: AsyncSession):
        for update_service in self.update_services:
            await update_service.update(session)
