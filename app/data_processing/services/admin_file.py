from abc import ABC, abstractmethod

from openpyxl import load_workbook

from app.config import Config
from app.db import async_session_maker
from app.models import Dish, Menu, Submenu
from app.utils import is_valid_uuid


class AdminFileWorksheetMixin:
    @property
    def worksheet(self):
        workbook = load_workbook(Config.ADMIN_FILE_PATH, data_only=True)
        return workbook.active


class AbstractAdminFileUpdatingService(AdminFileWorksheetMixin, ABC):
    @abstractmethod
    def create_missing_objects(self, session):
        ...


class AbstractAdminFileDeletingService(AdminFileWorksheetMixin, ABC):
    @abstractmethod
    def delete_redundant_objects(self, session):
        ...


class AdminFileService:

    def __init__(
            self,
            updating_service: list[AbstractAdminFileUpdatingService],
            # deletion_service: list[AbstractAdminFileDeletingService],
    ):
        self.updating_services = updating_service
        # self.deletion_services = deletion_service

    async def handle(self):
        async with async_session_maker() as session:
            for updating_service in self.updating_services:
                await updating_service.create_missing_objects(session)
            # for deletion_service in self.deletion_services:
            #     deletion_service.delete_redundant_objects()


class AdminFileMenuUpdatingService(AbstractAdminFileUpdatingService):
    id_index = 0
    title_index = 1
    description_index = 2

    async def create_missing_objects(self, session):
        for row in self.worksheet.iter_rows(values_only=True):
            if self.is_menu_row(row):
                self._create_menu(row, session)
        await session.commit()

    @classmethod
    def is_menu_row(cls, row):
        return is_valid_uuid(row[cls.id_index])

    def _create_menu(self, row, session):
        menu = Menu(
            id=row[self.id_index],
            title=row[self.title_index],
            description=row[self.description_index],
        )
        session.add(menu)


class AdminFileSubmenuUpdatingService(AbstractAdminFileUpdatingService):
    id_index = 1
    title_index = 2
    description_index = 3

    last_menu_id: str = ''

    async def create_missing_objects(self, session):
        for row in self.worksheet.iter_rows(values_only=True):
            if AdminFileMenuUpdatingService.is_menu_row(row):
                self.last_menu_id = row[AdminFileMenuUpdatingService.id_index]
            elif self.is_submenu_row(row):
                self._create_submenu(row, session)
        await session.commit()

    @classmethod
    def is_submenu_row(cls, row):
        return is_valid_uuid(row[cls.id_index])

    def _create_submenu(self, row, session):
        submenu = Submenu(
            id=row[self.id_index],
            title=row[self.title_index],
            description=row[self.description_index],
            menu_id=self.last_menu_id
        )
        session.add(submenu)


class AdminFileDishUpdatingService(AbstractAdminFileUpdatingService):
    id_index = 2
    title_index = 3
    description_index = 4
    price_index = 5

    last_submenu_id: str = ''

    async def create_missing_objects(self, session):
        for row in self.worksheet.iter_rows(values_only=True):
            if AdminFileSubmenuUpdatingService.is_submenu_row(row):
                self.last_submenu_id = row[AdminFileSubmenuUpdatingService.id_index]
            elif self.is_dish_row(row):
                self._create_dish(row, session)
        await session.commit()

    @classmethod
    def is_dish_row(cls, row):
        return is_valid_uuid(row[cls.id_index])

    def _create_dish(self, row, session):
        dish = Dish(
            id=row[self.id_index],
            title=row[self.title_index],
            description=row[self.description_index],
            price=row[self.price_index],
            submenu_id=self.last_submenu_id,
        )
        session.add(dish)
