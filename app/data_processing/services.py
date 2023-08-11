import pickle
from collections import namedtuple
from http import HTTPStatus
from typing import Generic, TypeVar

from fastapi import HTTPException
from openpyxl.reader.excel import load_workbook
from sqlalchemy.ext.asyncio import AsyncSession

from app.celery import celery
from app.common.services import AbstractBackgroundService
from app.config import Config
from app.data_processing.schemas import TaskCreated
from app.db import async_session_maker
from app.models import Dish, Menu, Submenu

TASK_NOT_FOUND_MESSAGE = 'Task not found or still being processing.'


TaskResultType = TypeVar('TaskResultType')


class AllMenusService(AbstractBackgroundService, Generic[TaskResultType]):

    async def get_task_result(self, task_id: str) -> TaskResultType:
        task = celery.AsyncResult(task_id)
        if task.ready():
            return pickle.loads(task.result)
        raise HTTPException(
            detail=TASK_NOT_FOUND_MESSAGE,
            status_code=HTTPStatus.ACCEPTED,
        )

    async def create_task(self) -> TaskCreated:
        task = self.task_function.delay()
        return TaskCreated(task_id=task.id)


class AdminFileService:
    Action = namedtuple('Action', ('is_menu', 'is_submenu', 'is_dish'))

    def __init__(self):
        self.last_menu: Menu = ...
        self.last_submenu: Submenu = ...

        self.menu_action = self.Action(True, False, False)
        self.submenu_action = self.Action(False, True, False)
        self.dish_action = self.Action(False, False, True)

    async def create_missing_objects(self) -> None:
        workbook = load_workbook(Config.ADMIN_FILE_PATH, data_only=True)
        worksheet = workbook.active

        actions = {
            self.menu_action: self.handle_menu,
            self.submenu_action: self.handle_submenu,
            self.dish_action: self.handle_dish,
        }

        async with async_session_maker() as session:
            for row in worksheet.iter_rows(values_only=True):
                action = self.get_action(row)

                await actions[action](row, session)

            await session.commit()

    def get_action(self, row: tuple) -> Action:
        is_menu = isinstance(row[0], int)
        is_submenu = isinstance(row[1], int)
        is_dish = isinstance(row[2], int)
        return self.Action(is_menu, is_submenu, is_dish)

    async def handle_menu(self, row: tuple, session: AsyncSession) -> None:
        title, description = row[1], row[2]
        menu = Menu(title=title, description=description)
        session.add(menu)
        self.last_menu = menu

    async def handle_submenu(self, row: tuple, session: AsyncSession) -> None:
        title, description = row[2], row[3]
        submenu = Submenu(title=title, description=description)
        self.last_menu.submenus.append(submenu)
        session.add(submenu)
        self.last_submenu = submenu

    async def handle_dish(self, row: tuple, session: AsyncSession) -> None:
        title, description, price = row[3], row[4], row[5]
        dish = Dish(title=title, description=description, price=price)
        self.last_submenu.dishes.append(dish)
        session.add(dish)
