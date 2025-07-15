import uuid

import pydantic


class BaseNotification(pydantic.BaseModel):
    pass


class UserRegisteredNotification(BaseNotification):
    id: uuid.UUID
