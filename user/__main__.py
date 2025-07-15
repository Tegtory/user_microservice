import contextlib

from user.infrastructure.logger import configure_logger
from user.presentors.grpc.server import Server


async def main() -> None:
    await asyncio.gather(Server().serve())


if __name__ == "__main__":
    import asyncio

    configure_logger()
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
