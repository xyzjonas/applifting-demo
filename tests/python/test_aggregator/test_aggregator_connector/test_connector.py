import uuid
from datetime import datetime

import mock
import pytest

from aggregator_common.models import create_all, drop_all
from aggregator_common.schemas import Token, Product
from aggregator_connector.client import RemoteClient
from test_aggregator.utils import MockResponse


@pytest.mark.asyncio
@mock.patch('aggregator_connector.token.TokenManager._refresh_token')
async def test_register_product(mocked_refresh, db_session, random_str):
    mocked_refresh.return_value = Token(value=random_str(), updated_at=datetime.utcnow())

    product_id = str(uuid.uuid4())
    product_to_be_registred = Product(
        id=product_id,
        name=random_str(),
        description=random_str(),
    )
    mocked_resp = MockResponse({'id': product_id}, 201)
    with mock.patch(
            "aggregator_connector.client.aiohttp.ClientSession.post", return_value=mocked_resp
    ):
        client = RemoteClient()
        response = await client.register_product(product_to_be_registred)
        assert response == product_to_be_registred

@pytest.fixture
def xxxx():
    create_all()
    yield
    drop_all()

# def test_overwrite2(xxxx):
#     from aggregator_common.models import Offer
#     idd = "asjdadjasdjlasjlkasd"
#     with Session(engine) as session:
#         session.add(Offer(
#             id=idd,
#             product_id="asadas",
#             items_in_stock=5,
#             price=1,
#         ))
#         session.commit()
#
#     with Session(engine) as session:
#         ofr = session.query(Offer).first()
#     assert ofr.items_in_stock == 5
#
#     with Session(engine) as session:
#         ofr = session.query(Offer).first()
#         setattr(ofr, 'items_in_stock', 155)
#         session.commit()
#     with Session(engine) as session:
#         ofr = session.query(Offer).first()
#         assert ofr.items_in_stock == 155




