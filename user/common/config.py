from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    SECRET_KEY: str

    RABBIT_HOST: str = "localhost"
    RABBIT_USER: str = "guest"
    RABBIT_PASSWORD: str = ""
    ENABLE_NOTIFICATIONS: bool = False

    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    CERT_PATH: str | None = None
    KEY_PATH: str | None = None

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def rabbit_url(self) -> str:
        return (
            "amqp://"
            f"{self.RABBIT_USER}:{self.RABBIT_PASSWORD}@{self.RABBIT_HOST}/"
        )


config = Config()
