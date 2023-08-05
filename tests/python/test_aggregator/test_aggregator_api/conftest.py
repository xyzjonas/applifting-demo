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


@pytest.fixture(scope='function')
def product(db_session, random_str):
    product = Product(
        name=f"Product ### {random_str()}",
        description=random_str(size=64)
    )
    db_session.add(product)
    db_session.commit()
    return product
