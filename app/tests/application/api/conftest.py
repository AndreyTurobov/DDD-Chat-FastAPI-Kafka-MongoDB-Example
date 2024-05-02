from fastapi import FastAPI
from fastapi.testclient import TestClient

import pytest

from application.api.main import create_app
from logic.init import init_container
from tests.fixtures import init_simple_container


@pytest.fixture
def app() -> FastAPI:
    app = create_app()
    app.dependency_overrides[init_container] = init_simple_container

    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app=app)
