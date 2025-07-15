from dishka import FromDishka
from grpc import ServicerContext, StatusCode

import user.auth_pb2 as proto
import user.auth_pb2_grpc as auth_grpc
from user.common.exceptions import AppError, NotFoundError
from user.domain.models import AuthUser
from user.domain.use_cases.user import UserUseCase
from user.infrastructure.injector import inject


class AuthService(auth_grpc.AuthServiceServicer):
    @inject
    async def register_telegram(
        self,
        user: AuthUser,
        context: ServicerContext,
        use_case: FromDishka[UserUseCase],
    ) -> proto.Empty:
        try:
            await use_case.register_by_telegram(
                user.telegram_id, user.username
            )
        except AppError:
            context.set_code(StatusCode.ALREADY_EXISTS)
        return proto.Empty()

    @inject
    async def login_telegram(
        self,
        user: AuthUser,
        context: ServicerContext,
        use_case: FromDishka[UserUseCase],
    ) -> proto.User | None:
        try:
            authorized = await use_case.get_by_telegram(user.telegram_id)
            return proto.User(
                id=str(authorized.id),
                is_admin=authorized.is_admin,
                is_banned=authorized.is_banned,
            )
        except NotFoundError:
            context.set_code(StatusCode.NOT_FOUND)
        return None
