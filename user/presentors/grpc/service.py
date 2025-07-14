import grpc

import user.auth_pb2 as auth
import user.auth_pb2_grpc as auth_grpc
from user.domain.models import AuthUser, User


class AuthService(auth_grpc.AuthServiceServicer):
    def __init__(self) -> None:
        self.users: list[User] = []

    def register_telegram(self, user: AuthUser, context: grpc.ServicerContext) -> None:
        self.users.append(
            User(username=user.username, telegram_id=user.telegram_id)
        )

    def register(self, user: AuthUser, context: grpc.ServicerContext) -> None:
        self.users.append(User(username=user.username, password=user.password))

    def login(self, user: AuthUser, context: grpc.ServicerContext) -> auth.User:
        for i in filter(
            lambda x: x.username == user.username
            and x.password == user.password,
            self.users,
        ):
            return auth.User(id=i.id)
        context.set_code(grpc.StatusCode.UNAUTHENTICATED)
        return auth.User(id="0")

    def login_telegram(self, user: AuthUser, context: grpc.ServicerContext) -> auth.User:
        for i in filter(lambda x: x.telegram_id == user.telegram_id, self.users):
            return auth.User(id=i.id)
        context.set_code(grpc.StatusCode.UNAUTHENTICATED)
        return auth.User(id="0")
