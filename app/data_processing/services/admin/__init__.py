from typing import TypeVar

from openpyxl import load_workbook  # type: ignore

from app.common.repository import AbstractRepository
from app.config import Config

AdminServicesRepositoryType = TypeVar('AdminServicesRepositoryType', bound=AbstractRepository)


class AdminWorksheetMixin:
    @property
    def worksheet(self):
        workbook = load_workbook(Config.ADMIN_FILE_PATH, data_only=True)
        return workbook.active
