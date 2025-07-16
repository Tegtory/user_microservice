from grpc import ServicerContext, StatusCode

from user.common.config import config


def is_request_authorized(context: ServicerContext) -> None:
    for _ in filter(
        lambda x: x.key == "auth" and x.value == config.SECRET_KEY,
        context.invocation_metadata(),
    ):
        return None
    context.set_code(StatusCode.UNAUTHENTICATED)
    return None
