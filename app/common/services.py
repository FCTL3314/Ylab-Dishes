from abc import ABC, abstractmethod

from app.common.repository import AbstractCRUDRepository


class AbstractCRUDService(ABC):
    def __init__(self, repository: AbstractCRUDRepository):
        self.repository = repository

    @abstractmethod
    def retrieve(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def list(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError
