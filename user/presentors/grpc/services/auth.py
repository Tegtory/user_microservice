import logging

from dishka import FromDishka
from grpc import ServicerContext, StatusCode

import user.auth_pb2 as proto
import user.auth_pb2_grpc as auth_grpc
from user.common.exceptions import AppError, NotFoundError
from user.domain.models import AuthUser, GetUser, LoginUser
from user.domain.use_cases.user import UserUseCase
from user.infrastructure.injector import inject

logger = logging.getLogger(__name__)


class AuthService(auth_grpc.AuthServiceServicer):
    @inject
    async def register_telegram(
        self,
        request: AuthUser,
        context: ServicerContext,
        use_case: FromDishka[UserUseCase],
    ) -> proto.User:
        logger.info("Received request on register_telegram")
        try:
            user = await use_case.register_by_telegram(
                AuthUser(
                    telegram_id=request.telegram_id,
                    username=request.username,
                    name=getattr(request, "name", None),
                ),
            )
            return proto.User(
                id=str(user.id),
                name=user.name,
                is_admin=user.is_admin,
                is_banned=user.is_banned,
            )
        except AppError:
            context.set_code(StatusCode.ALREADY_EXISTS)
            return None

    @inject
    async def login_telegram(
        self,
        request: LoginUser,
        context: ServicerContext,
        use_case: FromDishka[UserUseCase],
    ) -> proto.User | None:
        logger.info("Received request on login_telegram")
        try:
            user = await use_case.get_by_telegram(request.telegram_id)
        except NotFoundError:
            context.set_code(StatusCode.NOT_FOUND)
            return None
        return proto.User(
            id=str(user.id),
            name=user.name,
            is_admin=user.is_admin,
            is_banned=user.is_banned,
        )

    @inject
    async def get(
        self,
        request: GetUser,
        context: ServicerContext,
        use_case: FromDishka[UserUseCase],
    ) -> proto.User | None:
        logger.info("Received request on get")
        try:
            user = await use_case.get_by_id(request.id)
        except NotFoundError:
            context.set_code(StatusCode.NOT_FOUND)
            return None
        return proto.User(
            id=str(user.id),
            name=user.name,
            is_admin=user.is_admin,
            is_banned=user.is_banned,
        )
