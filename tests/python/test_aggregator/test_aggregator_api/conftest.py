import pytest
from starlette.testclient import TestClient

from aggregator_api.api.v1.common.dependencies import logged_in
from aggregator_api.app import app
from aggregator_api.auth import User


# Ignore auth middleware...
app.dependency_overrides[logged_in] = lambda: User(username="test-user", password="always authenticated")


@pytest.fixture(scope="session")
def base_route() -> str:
    return '/api/v1'


@pytest.fixture(scope="function")
def test_client() -> TestClient:
    yield TestClient(app)



