import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from mixer.auto import mixer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.config import Config
from app.db import get_async_session
from app.main import app
from app.models import Menu, Submenu

TEST_SQLALCHEMY_URI = (
    f"postgresql+asyncpg://"
    f"{Config.TEST_DATABASE_USER}:"
    f"{Config.TEST_DATABASE_PASSWORD}@"
    f"{Config.TEST_DATABASE_HOST}/"
    f"{Config.TEST_DATABASE_NAME}"
)
test_async_engine = create_async_engine(TEST_SQLALCHEMY_URI)
async_session_maker = sessionmaker(bind=test_async_engine, class_=AsyncSession)
SQLModel.metadata.bind = test_async_engine


async def override_get_async_session():
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with test_async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with test_async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def session():
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator | None:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture()
async def menu(session: AsyncSession):
    menu = mixer.blend("app.models.Menu")
    session.add(menu)
    await session.commit()
    await session.refresh(menu)
    yield menu
    await session.delete(menu)
    await session.commit()


@pytest.fixture()
async def submenu(menu: Menu, session: AsyncSession):
    submenu = mixer.blend("app.models.Submenu", menu_id=menu.id)
    session.add(submenu)
    await session.commit()
    await session.refresh(submenu)
    yield submenu
    await session.delete(submenu)
    await session.commit()


@pytest.fixture()
async def dish(submenu: Submenu, session: AsyncSession):
    dish = mixer.blend("app.models.Dish", submenu_id=submenu.id)
    session.add(dish)
    await session.commit()
    await session.refresh(dish)
    yield dish
    await session.delete(dish)
    await session.commit()
