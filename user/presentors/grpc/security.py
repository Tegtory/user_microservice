import logging

from grpc import ServicerContext, StatusCode

from user.common.config import config

logger = logging.getLogger(__name__)


def is_request_authorized(context: ServicerContext) -> bool:
    for _ in filter(
        lambda x: x.key == "auth" and x.value == config.SECRET_KEY,
        context.invocation_metadata(),
    ):
        return True
    logger.warning("Unauthorized request:")
    logger.warning(context.auth_context())
    logger.warning(context.invocation_metadata())
    context.set_code(StatusCode.UNAUTHENTICATED)
    return False
