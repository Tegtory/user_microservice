from dishka import FromDishka
from grpc import ServicerContext, StatusCode

import user.auth_pb2 as proto
import user.auth_pb2_grpc as auth_grpc
from user.common.exceptions import AppError, NotFoundError
from user.domain.models import AuthUser, LoginUser
from user.domain.use_cases.user import UserUseCase
from user.infrastructure.injector import inject
from user.presentors.grpc.security import is_request_authorized


class AuthService(auth_grpc.AuthServiceServicer):
    @inject
    async def register_telegram(
        self,
        user: AuthUser,
        context: ServicerContext,
        use_case: FromDishka[UserUseCase],
    ) -> proto.Empty:
        if not is_request_authorized(context):
            return None
        try:
            await use_case.register_by_telegram(
                AuthUser(
                    telegram_id=user.telegram_id,
                    username=user.username,
                    name=user.name,
                ),
            )
        except AppError:
            context.set_code(StatusCode.ALREADY_EXISTS)
        return proto.Empty()

    @inject
    async def login_telegram(
        self,
        user: LoginUser,
        context: ServicerContext,
        use_case: FromDishka[UserUseCase],
    ) -> proto.User | None:
        if not is_request_authorized(context):
            return None
        try:
            authorized = await use_case.get_by_telegram(user.telegram_id)
        except NotFoundError:
            context.set_code(StatusCode.NOT_FOUND)
            return None
        return proto.User(
            id=str(authorized.id),
            name=authorized.name,
            is_admin=authorized.is_admin,
            is_banned=authorized.is_banned,
        )
