from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
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
