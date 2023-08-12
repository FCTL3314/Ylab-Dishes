from abc import ABC, abstractmethod
from typing import Generic

from sqlalchemy.ext.asyncio import AsyncSession

from app.data_processing.services.admin import (
    AdminServicesRepositoryType,
    AdminWorksheetMixin,
)


class AbstractAdminDeletingService(AdminWorksheetMixin, ABC, Generic[AdminServicesRepositoryType]):
    def __init__(self, repository: AdminServicesRepositoryType):
        self.repository = repository

    @abstractmethod
    def delete_redundant_objects(self, session: AsyncSession):
        ...
