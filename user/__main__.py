import argparse
import contextlib

from user.infrastructure.logger import configure_logger
from user.presentors.grpc.server import Server


async def main(args: argparse.Namespace) -> None:
    await asyncio.gather(Server(**args.__dict__).serve())


if __name__ == "__main__":
    import asyncio

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="[::]", help="host, [::] - all")
    parser.add_argument("--port", default=5000, type=int, help="port")
    argv = parser.parse_args()

    configure_logger()
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main(argv))
