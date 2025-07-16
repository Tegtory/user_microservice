from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class Database:
    def __init__(self, url: str) -> None:
        self.engine = create_async_engine(url=url)
        self.maker = async_sessionmaker(self.engine, expire_on_commit=False)

    async def get_session(self) -> AsyncSession:
        return self.maker()
