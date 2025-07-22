import logging
from concurrent import futures
from typing import Self

import grpc

import user.auth_pb2_grpc as auth_grpc
from user.common.config import config
from user.presentors.grpc.interceptor import ApiKeyInterceptor
from user.presentors.grpc.services.auth import AuthService

logger = logging.getLogger(__name__)


class Server:
    def __init__(
        self, port: int = 5000, host: str = "[::]", max_workers: int = 10
    ) -> None:
        self._port = port
        self._host = host
        self._server = grpc.aio.server(
            futures.ThreadPoolExecutor(max_workers=max_workers),
            interceptors=[ApiKeyInterceptor(config.SECRET_KEY)],
        )
        auth_grpc.add_AuthServiceServicer_to_server(  # type: ignore
            AuthService(), self._server
        )
        if config.KEY_PATH and config.CERT_PATH:
            with open(config.KEY_PATH, "rb") as f:
                private_key = f.read()
            with open(config.CERT_PATH, "rb") as f:
                certificate = f.read()
            self._server.add_secure_port(
                f"{self._host}:{self._port}",
                grpc.ssl_server_credentials([(private_key, certificate)]),
            )
        else:
            self._server.add_insecure_port(f"{self._host}:{self._port}")
        logger.info("Server initialized...")

    async def serve(self) -> None:
        await self._server.wait_for_termination()

    async def __aenter__(self) -> Self:
        await self._server.start()
        logger.info("Listening on %s", f"{self._host}:{self._port}")
        return self

    async def __aexit__(
        self, exc_type: type[Exception], exc_val: Exception, exc_tb: str
    ) -> None:
        await self._server.stop(5)
        logger.info("Server is stopped")
