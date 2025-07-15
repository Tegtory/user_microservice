import uuid
from datetime import datetime

from sqlalchemy import UUID, Boolean, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from user.infrastructure.repositories.slqalchemy import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)

    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
