import uuid
from typing import Protocol


class ProfileRepository(Protocol):
    async def set_name(self, uid: uuid.UUID, name: str) -> None:
        pass
