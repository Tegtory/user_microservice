import contextlib

from user.infrastructure.logger import configure_logger


async def main() -> None:
    pass


if __name__ == "__main__":
    import asyncio

    configure_logger()
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
