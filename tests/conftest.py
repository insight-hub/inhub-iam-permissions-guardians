from os import environ

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient


environ["APP_ENV"] = "test"


@pytest.fixture
def app() -> FastAPI:
    from app.main import get_application  # local import for testing purpose

    app = get_application()

    client = TestClient(app)

    yield client
