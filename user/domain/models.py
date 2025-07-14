import uuid

from pydantic import BaseModel, Field


class User(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    telegram_id: int | None = None
    username: str | None = None
    password: str | None = None
    permissions: list[str] | None = None


class AuthUser(BaseModel):
    telegram_id: int | None = None
    username: str | None = None
    password: str | None = None
