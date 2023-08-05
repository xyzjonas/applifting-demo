import os.path
import uuid

import pytest

from aggregator_api.api.v1.common.schemas import ProductCreate, ProductUpdate
from aggregator_common.schemas import Product as ProductRead
from test_aggregator.utils import assert_response
from aggregator_common.models import Product


@pytest.fixture(scope='function', params=[0, 5, 100])
def products(request, db_session):
    for index in range(request.param):
        db_session.add(
            Product(
                name=f"Product #{index}",
                description=f"Description for product {index}"
            )
        )
    db_session.commit()
    return request.param


def test_get_products(test_client, base_route, products):
    response = test_client.get(os.path.join(base_route, 'products'))
    response.raise_for_status()
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data['items'], list)
    assert response_data['total'] == products


def test_get_product(test_client, base_route, product):
    response = test_client.get(os.path.join(base_route, 'products'))
    response.raise_for_status()
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['total'] == 1

    response = test_client.get(os.path.join(base_route, 'products', product.id))
    response.raise_for_status()


@pytest.mark.skip(reason="Mock the remote client here as well.")
@pytest.mark.usefixtures('db_session')
def test_add_product(test_client, base_route, random_str):
    create_data = ProductCreate(name=random_str(), description=random_str())
    response = assert_response(
        test_client.post(os.path.join(base_route, 'products'), json=create_data.model_dump())
    )
    assert response.status_code == 201
    product = ProductRead(**response.json())
    assert product
    assert product.id
    assert product.name == create_data.name
    assert product.description == create_data.description


def test_edit_product(test_client, base_route, product, random_str):
    update_data = ProductUpdate(name=random_str(), description=random_str())
    response = assert_response(
        test_client.put(
            os.path.join(base_route, 'products', product.id),
            json=update_data.model_dump()
        )
    )
    assert response.status_code == 200
    product = ProductRead(**response.json())
    assert product
    assert product.id == product.id
    assert product.name == update_data.name
    assert product.description == update_data.description


@pytest.mark.usefixtures('db_session')
def test_edit_not_found(test_client, base_route, random_str):
    update_data = ProductUpdate(name=random_str(), description=random_str())

    response = test_client.put(
        os.path.join(base_route, 'products', str(uuid.uuid4())),
        json=update_data.model_dump()
    )
    assert response.status_code == 404


def test_delete_product(test_client, base_route, product, random_str):
    response = test_client.get(os.path.join(base_route, 'products', product.id))
    assert response.status_code == 200

    response = assert_response(
        test_client.delete(os.path.join(base_route, 'products', product.id))
    )
    assert response.status_code == 200

    response = test_client.get(os.path.join(base_route, 'products', product.id))
    assert response.status_code == 404
