from unittest.mock import AsyncMock, MagicMock

import pytest

from user.common.exceptions import AppError, NotFoundError
from user.domain.models import AuthUser
from user.domain.use_cases.user import User, UserUseCase


@pytest.fixture()
def notif_repo() -> MagicMock:
    mock = MagicMock()
    mock.about__user_registered = AsyncMock()
    return mock


@pytest.fixture()
def user_repo() -> MagicMock:
    mock = MagicMock()
    mock.get_by_tg_id = AsyncMock()
    mock.create = AsyncMock()
    return mock


@pytest.mark.asyncio()
async def test__create_user__success(
    user_repo: MagicMock, notif_repo: MagicMock
) -> None:
    user_repo.get_by_tg_id = AsyncMock(side_effect=NotFoundError)
    user_repo.create.return_value = User(telegram_id=1, username="1")

    use_case = UserUseCase(user_repo, notif_repo)
    await use_case.register_by_telegram(AuthUser(telegram_id=1, username="1"))

    user_repo.get_by_tg_id.assert_called_with(1)
    notif_repo.about__user_registered.assert_called_once()


@pytest.mark.asyncio()
async def test__registered__failure_user_exists(
    user_repo: MagicMock, notif_repo: MagicMock
) -> None:
    use_case = UserUseCase(user_repo, notif_repo)

    with pytest.raises(AppError):
        await use_case.register_by_telegram(
            AuthUser(telegram_id=1, username="1"),
        )
    user_repo.get_by_tg_id.assert_called_with(1)
    notif_repo.about__user_registered.assert_not_called()


@pytest.mark.asyncio()
async def test__get_user__success(
    user_repo: MagicMock, notif_repo: MagicMock
) -> None:
    user = User(telegram_id=1, username="1")
    user_repo.get_by_tg_id.return_value = user
    use_case = UserUseCase(user_repo, notif_repo)

    result = await use_case.get_by_telegram(1)
    user_repo.get_by_tg_id.assert_called_with(1)
    assert result == user
