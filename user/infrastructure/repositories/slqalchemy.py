from sqlalchemy import Engine, create_engine


class DatabaseService:
    @staticmethod
    async def get_engine() -> Engine:
        return create_engine("sqlite+pysqlite:///:memory:", echo=True)
