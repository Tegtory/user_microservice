import uuid

from pydantic import BaseModel, Field


class User(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    telegram_id: int
    username: str
    name: str | None = None
    is_admin: bool = False
    is_banned: bool = False


class AuthUser(BaseModel):
    telegram_id: int
    username: str
    name: str | None = None


class LoginUser(BaseModel):
    telegram_id: int


class ChangeName(BaseModel):
    id: uuid.UUID
    name: str
