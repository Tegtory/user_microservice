from sqlalchemy import create_engine, Engine


class DatabaseService:
    @staticmethod
    async def get_engine() -> Engine:
        return create_engine("sqlite+pysqlite:///:memory:", echo=True)
