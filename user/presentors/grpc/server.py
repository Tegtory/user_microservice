import contextlib
import logging
from concurrent import futures

import grpc

import user.auth_pb2_grpc as auth_grpc
from user.presentors.grpc.service import AuthService

logger = logging.getLogger(__name__)


class Server:
    def __init__(
        self, port: int = 5000, host: str = "[::]", max_workers: int = 3
    ) -> None:
        self._port = port
        self._host = host
        self._server = grpc.aio.server(
            futures.ThreadPoolExecutor(max_workers=max_workers)
        )
        auth_grpc.add_AuthServiceServicer_to_server(
            AuthService(), self._server
        )
        self._server.add_insecure_port(f"{self._host}:{self._port}")
        logger.info("Server initialized...")

    async def serve(self) -> None:
        await self._server.start()
        logger.info(f"Listening on {self._host}:{self._port}")
        logger.info("Press CTRL+C to stop...")

        with contextlib.suppress(KeyboardInterrupt):
            await self._server.wait_for_termination()
        await self._server.stop(None)
        logger.info("Server is stopped")
