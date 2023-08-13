from typing import TypeVar

from app.common.repository import AbstractRepository

AdminServicesRepositoryType = TypeVar('AdminServicesRepositoryType', bound=AbstractRepository)
