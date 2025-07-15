class AppError(Exception):
    pass


class NotAuthenticatedError(AppError):
    pass


class NotFoundError(AppError):
    pass
