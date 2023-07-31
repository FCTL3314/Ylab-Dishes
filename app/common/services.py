from abc import ABC, abstractmethod


class AbstractCRUDService(ABC):
    def __init__(self, repository):
        self.repository = repository()

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
