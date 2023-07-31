from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def all(self, *args, **kwargs):
        raise NotImplementedError
