from pytest import fixture
from punq import Container

from infra.repositories.messages.base import BaseChatsRepository
from logic.mediator import Mediator
from tests.fixtures import init_simple_container


@fixture(scope="function")
def container() -> Container:
    return init_simple_container()


@fixture()
def mediator(container: Container) -> Mediator:

    return container.resolve(Mediator)


@fixture()
def chat_repository(container: Container) -> BaseChatsRepository:
    return container.resolve(BaseChatsRepository)
