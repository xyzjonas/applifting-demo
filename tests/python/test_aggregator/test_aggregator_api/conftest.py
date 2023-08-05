import pytest
from starlette.testclient import TestClient

from aggregator_api.app import app
from aggregator_common.models import Product


@pytest.fixture(scope="session")
def base_route() -> str:
    return '/api/v1'


@pytest.fixture(scope="function")
def test_client() -> TestClient:
    yield TestClient(app)



