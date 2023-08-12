from app.data_processing.services.admin.updating_services import (
    AbstractAdminUpdatingService,
)
from app.db import async_session_maker


class AdminFileService:

    def __init__(
            self,
            updating_services: list[AbstractAdminUpdatingService],
            # deletion_services: list[AbstractAdminFileDeletingService],
    ):
        self.updating_services = updating_services
        # self.deletion_services = deletion_services

    async def handle(self):
        async with async_session_maker() as session:
            for updating_service in self.updating_services:
                await updating_service.create_missing_objects(session)
            # for deletion_service in self.deletion_services:
            #     deletion_service.delete_redundant_objects()
