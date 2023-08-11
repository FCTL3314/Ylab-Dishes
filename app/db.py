import asyncio
from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from app.config import Config

SQLALCHEMY_URI = (
    f'postgresql+asyncpg://'
    f'{Config.DATABASE_USER}:'
    f'{Config.DATABASE_PASSWORD}@'
    f'{Config.DATABASE_HOST}/'
    f'{Config.DATABASE_NAME}'
)
async_engine = create_async_engine(SQLALCHEMY_URI)
async_session_maker = sessionmaker(bind=async_engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session


@asynccontextmanager
async def scoped_session():
    scoped_factory = async_scoped_session(
        async_session_maker,
        scopefunc=current_task,
    )
    try:
        async with scoped_factory() as session:
            yield session
    finally:
        await scoped_factory.remove()


scoped_loop = asyncio.new_event_loop()
