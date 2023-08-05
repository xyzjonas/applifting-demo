import string
import random

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from aggregator_common import configuration
from aggregator_common.models import create_all, drop_all, Product, Offer


@pytest.fixture(scope='function')
def random_str():
    def _inner(size=12):
        return ''.join([random.choice(string.ascii_lowercase + ' ') for _ in range(size)])
    return _inner


@pytest.fixture(scope='function')
def db_session():
    create_all()
    yield Session(create_engine(configuration.api.database_uri))
    drop_all()


@pytest.fixture(scope='function')
def product(db_session, random_str):
    product = Product(
        name=f"Product ### {random_str()}",
        description=random_str(size=64)
    )
    db_session.add(product)
    db_session.commit()
    return product


@pytest.fixture(scope='function', params=[0, 5, 101])
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
