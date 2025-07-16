import uuid

from user.common.exceptions import NotFoundError
from user.domain.interfaces.profile import ProfileRepository
from user.domain.interfaces.user import UserRepository


class UserUseCase:
    def __init__(
        self,
        repository: UserRepository,
        profile: ProfileRepository,
    ) -> None:
        self.repository = repository
        self.profile = profile

    async def change_name(self, uid: uuid.UUID, name: str) -> None:
        user = await self.repository.get(uid)
        if not user:
            raise NotFoundError
        await self.profile.set_name(
            user.id,
            name,
        )
