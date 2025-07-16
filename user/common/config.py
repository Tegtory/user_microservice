from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    SECRET_KEY: str
    RABBIT_HOST: str = "localhost"
    RABBIT_PASSWORD: str = "guest"
    RABBIT_USER: str = "guest"
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    def get_db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    def get_rabbit_url(self) -> str:
        return (
            "amqp://"
            f"{self.RABBIT_USER}:{self.RABBIT_PASSWORD}@{self.RABBIT_HOST}/"
        )


config = Config()
