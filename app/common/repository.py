from abc import abstractmethod, ABC

from sqlmodel import Session

from app.db import get_session


class BaseRepository(ABC):
    def __init__(self):
        self.session: Session = self.get_session()

    @abstractmethod
    def get_session(self) -> Session:
        pass


class BaseCRUDRepository(BaseRepository):
    def get_session(self) -> Session:
        return next(get_session())

    @abstractmethod
    def retrieve(self, *args, **kwargs):
        pass

    @abstractmethod
    def list(self, *args, **kwargs):
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass
