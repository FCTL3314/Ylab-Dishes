from app.data_processing.services.admin.updating_services import BaseAdminService
from app.db import async_session_maker


class AdminFileService:

    def __init__(self, updating_services: list[BaseAdminService]):
        self.services = updating_services

    async def handle(self):
        async with async_session_maker() as session:
            for updating_service in self.services:
                await updating_service.update(session)
