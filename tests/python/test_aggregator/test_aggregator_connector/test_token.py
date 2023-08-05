from datetime import datetime, timedelta

import pytest
import mock
from mock.mock import MagicMock

from aggregator_common.models import Token as TokenDb
from aggregator_connector.token import TokenManager
from aggregator_common.schemas import Token
from aggregator_common.configuration import get_configuration


@pytest.fixture(scope='function')
def valid_token(db_session, random_str):
    tok = TokenDb(key=1, value=random_str(), updated_at=datetime.utcnow())
    db_session.add(tok)
    db_session.commit()
    return Token(
        updated_at=tok.updated_at,
        value=tok.value,
    )


@pytest.fixture(scope='function', params=["expired", "none"])
def invalid_token(db_session, request, random_str):
    if request.param == "none":
        return
    expired_datetime = datetime.utcnow() - timedelta(seconds=get_configuration().token_validity_secs + 1)  # noqa: E505
    tok = TokenDb(key=1, value=random_str(), updated_at=expired_datetime)
    db_session.add(tok)
    db_session.commit()
    assert tok.updated_at == expired_datetime
    return Token(
        updated_at=tok.updated_at,
        value=tok.value,
    )


@pytest.mark.asyncio
async def test_token_query(valid_token):
    token_warden = TokenManager()
    token = await token_warden.get_token()
    assert token.value == valid_token.value
    assert not token_warden.token_expired


@pytest.mark.asyncio
@mock.patch('aggregator_connector.token.TokenManager._refresh_token')
async def test_token_regen(mock_request: MagicMock, invalid_token, random_str):
    token_value = random_str()
    mock_request.return_value = Token(value=token_value, updated_at=datetime.utcnow())

    token_warden = TokenManager()
    assert token_warden.token_expired
    assert await token_warden.get_token()
    assert await token_warden.get_token()
    assert await token_warden.get_token()
    mock_request.assert_called_once()
    token = await token_warden.get_token()
    assert token.value == token_value
    assert not token_warden.token_expired
