import logging

from dishka import Provider, Scope, make_async_container

logger = logging.getLogger(__name__)

provider = Provider(scope=Scope.APP)

container = make_async_container(provider)
