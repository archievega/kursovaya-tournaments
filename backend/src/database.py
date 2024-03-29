from sqlalchemy.orm import DeclarativeBase
from collections.abc import AsyncGenerator
from sqlalchemy import MetaData

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

base_metadata = MetaData(schema="public")

class Base(DeclarativeBase):
    pass

engine = create_async_engine(settings.db_url_postgresql, echo=False)
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
