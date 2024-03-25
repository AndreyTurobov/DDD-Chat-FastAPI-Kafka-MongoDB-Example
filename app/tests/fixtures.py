from punq import Container, Scope

from infra.repositories.messages import BaseChatRepository, MemoryChatRepository
from logic.init import _init_container


def init_simple_container() -> Container:
    container = _init_container()
    container.register(BaseChatRepository, MemoryChatRepository, scope=Scope.singleton)

    return container
