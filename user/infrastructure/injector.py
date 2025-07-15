from collections.abc import Callable
from typing import Any

from dishka import AsyncContainer
from dishka.integrations.base import wrap_injection

from .di import container


def inject(func: Callable) -> Any:
    def container_getter(
        _args: tuple[Any, ...], _kwargs: dict[str, Any]
    ) -> AsyncContainer:
        return container

    return wrap_injection(
        func=func, container_getter=container_getter, is_async=True
    )
