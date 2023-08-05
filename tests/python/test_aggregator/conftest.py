import string
import random

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from aggregator_common.configuration import get_configuration
from aggregator_common.models import create_all, drop_all


@pytest.fixture(scope='function')
def random_str():
    def _inner(size=12):
        return ''.join([random.choice(string.ascii_lowercase + ' ') for _ in range(size)])
    return _inner


@pytest.fixture(scope='function')
def db_session():
    create_all()
    yield Session(create_engine(get_configuration().database_uri))
    drop_all()
