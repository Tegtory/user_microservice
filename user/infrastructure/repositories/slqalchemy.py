from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from user.common.config import config

DB_URL = config.get_db_url()


class Database:
    def __init__(self) -> None:
        self.engine = create_async_engine(url=DB_URL)
        self.maker = async_sessionmaker(self.engine, expire_on_commit=False)

    async def get_session(self) -> AsyncSession:
        return self.maker()


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
