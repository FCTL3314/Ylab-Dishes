from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def all(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def scalar_all(self, *args, **kwargs):
        raise NotImplementedError


class AbstractCRUDRepository(AbstractRepository):
    @abstractmethod
    def get_by_id(self, *args, **kwargs):
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
