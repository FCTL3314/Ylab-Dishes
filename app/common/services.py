from abc import ABC, abstractmethod

from celery.local import PromiseProxy

from app.common.repository import AbstractCRUDRepository


class AbstractRetrieveService(ABC):
    @abstractmethod
    def retrieve(self, *args, **kwargs):
        raise NotImplementedError


class AbstractListService(ABC):
    @abstractmethod
    def list(self, *args, **kwargs):
        raise NotImplementedError


class AbstractCreateService(ABC):
    @abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError


class AbstractUpdateService(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError


class AbstractDeleteService(ABC):
    @abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError


class AbstractCRUDService(
    AbstractRetrieveService,
    AbstractListService,
    AbstractCreateService,
    AbstractUpdateService,
    AbstractDeleteService,
    ABC,
):
    def __init__(self, repository: AbstractCRUDRepository):
        self.repository = repository


class AbstractBackgroundService(ABC):
    def __init__(self, task_function: PromiseProxy):
        self.task_function = task_function

    @abstractmethod
    def get_task_result(self, task_id: str):
        raise NotImplementedError

    @abstractmethod
    def create_task(self, *args, **kwargs):
        raise NotImplementedError
