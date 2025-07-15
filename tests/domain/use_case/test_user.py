from unittest.mock import AsyncMock, MagicMock

import pytest

from user.domain.use_cases.user import User, UserUseCase


@pytest.fixture
def notif_repo() -> MagicMock:
    mock = MagicMock()
    mock.about__user_registered = AsyncMock()
    return mock


@pytest.fixture
def user_repo() -> MagicMock:
    mock = MagicMock()
    mock.get_by_telegram_id = AsyncMock()
    mock.create = AsyncMock()
    return mock


@pytest.mark.asyncio
async def test__successfully_registered(
    user_repo: MagicMock, notif_repo: MagicMock
) -> None:
    mock_user = User(telegram_id=1, username="1")
    user_repo.get_by_telegram_id.return_value = None
    user_repo.create.return_value = mock_user
    use_case = UserUseCase(user_repo, notif_repo)
    await use_case.register_by_telegram(1, "1")

    user_repo.get_by_telegram_id.assert_called_with(1)
    notif_repo.about__user_registered.assert_called_once()
