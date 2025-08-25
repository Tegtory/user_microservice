from functools import partial
from typing import Any

from grpc import (
    HandlerCallDetails,
    StatusCode,
    aio,
    unary_unary_rpc_method_handler,
)


class ApiKeyInterceptor(aio.ServerInterceptor):
    def __init__(self, valid_api_key: str) -> None:
        self.valid_api_key = valid_api_key

    async def intercept_service(
        self, continuation: partial, handler_call_details: HandlerCallDetails
    ) -> Any:
        metadata = dict(handler_call_details.invocation_metadata)
        if metadata.get("auth") != self.valid_api_key:
            return unary_unary_rpc_method_handler(self.deny)
        return await continuation(handler_call_details)

    @staticmethod
    async def deny(_: bytes, context: aio.ServicerContext) -> None:
        await context.abort(StatusCode.UNAUTHENTICATED, "Токен не найден")
