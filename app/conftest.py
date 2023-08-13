import asyncio
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from mixer.auto import mixer
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.config import TestConfig
from app.db import get_async_session
from app.main import app
from app.models import Menu, Submenu
from app.redis import redis

TEST_SQLALCHEMY_URI = (
    f'postgresql+asyncpg://'
    f'{TestConfig.DATABASE_USER}:'
    f'{TestConfig.DATABASE_PASSWORD}@'
    f'{TestConfig.DATABASE_HOST}/'
    f'{TestConfig.DATABASE_NAME}'
)
test_async_engine = create_async_engine(TEST_SQLALCHEMY_URI)
async_session_maker = sessionmaker(bind=test_async_engine, class_=AsyncSession)
SQLModel.metadata.bind = test_async_engine  # type: ignore


async def override_get_async_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database() -> AsyncGenerator:
    """
    Creates the test database when tests run, deletes
    when tests finished.
    """
    async with test_async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with test_async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as async_client:
        yield async_client


async def create_test_object(model_path: str, session: AsyncSession, **kwargs) -> SQLModel:
    """
    Creates a test object that will be deleted when
    the test is complete.
    """
    obj = mixer.blend(model_path, **kwargs)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


async def remove_test_object(obj: SQLModel | Row | None, session: AsyncSession) -> None:
    await session.delete(obj)
    await session.commit()


@pytest.fixture()
async def menu(session: AsyncSession) -> AsyncGenerator[SQLModel, None]:
    menu = await create_test_object('app.models.Menu', session)
    yield menu
    await remove_test_object(menu, session)


@pytest.fixture()
async def submenu(menu: Menu, session: AsyncSession) -> AsyncGenerator[SQLModel, None]:
    submenu = await create_test_object('app.models.Submenu', session, menu_id=menu.id)
    yield submenu
    await remove_test_object(submenu, session)


@pytest.fixture()
async def dish(submenu: Submenu, session: AsyncSession) -> AsyncGenerator[SQLModel, None]:
    dish = await create_test_object('app.models.Dish', session, submenu_id=submenu.id)
    yield dish
    await remove_test_object(dish, session)


@pytest.fixture(autouse=True)
async def clear_cache() -> None:
    """
    Clear all cache before each test run.
    """
    await redis.flushall()
