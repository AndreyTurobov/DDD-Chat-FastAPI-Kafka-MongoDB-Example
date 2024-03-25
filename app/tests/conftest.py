from pytest import fixture
from punq import Container

from app.infra.repositories.messages import BaseChatRepository
from app.logic.mediator import Mediator
from app.tests.fixtures import init_simple_container


@fixture(scope="function")
def container() -> Container:
    return init_simple_container()


@fixture()
def mediator(container: Container) -> Mediator:

    return container.resolve(Mediator)


@fixture()
def chat_repository(container: Container) -> BaseChatRepository:
    return container.resolve(BaseChatRepository)
