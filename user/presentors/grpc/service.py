import grpc
from dishka import FromDishka

import user.auth_pb2 as proto
import user.auth_pb2_grpc as auth_grpc
from user.common.exceptions import AppError
from user.domain.models import AuthUser
from user.domain.use_cases.user import UserUseCase
from user.infrastructure.injector import inject


class AuthService(auth_grpc.AuthServiceServicer):
    @inject
    async def register_telegram(
        self,
        user: AuthUser,
        context: grpc.ServicerContext,
        use_case: FromDishka[UserUseCase],
    ) -> proto.Empty:
        if not user.telegram_id or not user.username:
            raise AppError
        await use_case.register_by_telegram(user.telegram_id, user.username)
        return proto.Empty()

    async def register(
        self, user: AuthUser, context: grpc.ServicerContext
    ) -> None:
        return None

    async def login(
        self, user: AuthUser, context: grpc.ServicerContext
    ) -> None:
        return None

    @inject
    async def login_telegram(
        self,
        user: AuthUser,
        context: grpc.ServicerContext,
        use_case: FromDishka[UserUseCase],
    ) -> proto.User:
        if not user.telegram_id:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return proto.User(id="0")
        authorized = await use_case.login_by_telegram(user.telegram_id)
        if not authorized:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return proto.User(id="0")
        return proto.User(id=str(authorized.id))
