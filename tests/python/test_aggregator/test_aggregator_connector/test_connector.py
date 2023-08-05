import uuid
from datetime import datetime

import pytest

import mock

from aggregator_common.schemas import Token
from aggregator_connector.client import AggregatorClient
from test_aggregator.utils import MockResponse


@pytest.mark.asyncio
@mock.patch('aggregator_connector.token.TokenManager._refresh_token')
async def test_register_product(mocked_refresh, db_session, random_str):
    mocked_refresh.return_value = Token(value=random_str(), updated_at=datetime.utcnow())

    product_id = str(uuid.uuid4())
    request_data = {
        "product_id": product_id,
        "product_name": random_str(),
        "product_description": random_str(),
    }
    mocked_resp = MockResponse({'id': product_id}, 201)
    with mock.patch(
            "aggregator_connector.client.aiohttp.ClientSession.post", return_value=mocked_resp
    ) as mocked_resp:
        client = AggregatorClient()
        response = await client.register_product(**request_data)
        h = mocked_resp.response_data
        assert response == {'id': product_id}
