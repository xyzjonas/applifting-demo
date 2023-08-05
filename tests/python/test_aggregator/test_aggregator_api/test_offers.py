import posixpath

import pytest

from aggregator_common.models import Offer


@pytest.fixture(scope='function', params=[5])
def offers(request, db_session, product):
    offers = []
    for index in range(request.param):
        offers.append(
            Offer(
                price=index,
                items_in_stock=index,
                product_id=product.id,
            )
        )
    db_session.add_all(offers)
    db_session.commit()
    return offers


def test_get_offers(test_client, base_route, product, offers):
    response = test_client.get(posixpath.join(base_route, 'products', product.id))
    response.raise_for_status()
    assert response.status_code == 200

    response = test_client.get(posixpath.join(base_route, 'offers'))
    response.raise_for_status()
    assert response.status_code == 200
    actual_offers = response.json()
    assert isinstance(actual_offers['items'], list)
    assert actual_offers['total'] == len(offers)


def test_get_product_offers(test_client, base_route, product, offers):
    response = test_client.get(posixpath.join(base_route, 'products', product.id))
    response.raise_for_status()
    assert response.status_code == 200

    response = test_client.get(posixpath.join(base_route, 'offers'))
    response.raise_for_status()
    assert response.status_code == 200
    actual_offers = response.json()
    assert isinstance(actual_offers['items'], list)
    assert actual_offers['total'] == len(offers)

    response = test_client.get(posixpath.join(base_route, 'products', product.id, 'offers'))
    response.raise_for_status()
    assert response.status_code == 200
    actual_offers = response.json()
    assert isinstance(actual_offers['items'], list)
    assert actual_offers['total'] == len(offers)
