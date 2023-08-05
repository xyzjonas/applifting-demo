import posixpath
from datetime import datetime, timedelta

import aiohttp
from loguru import logger
from sqlalchemy.orm import Session

from aggregator_common import configuration
from aggregator_common.exceptions import TokenError
from aggregator_common.models import Token as TokenDb
from aggregator_common.models import engine
from aggregator_common.schemas import Token


class TokenManager:
    """Manages access token stashing/retrieval/refresh."""

    _token: Token | None
    token_key: int = 1

    request_token_url = posixpath.join(configuration.connector.cloud_uri, "api/v1/auth")

    def __init__(self) -> None:
        self._token = None

    async def _refresh_token(self, db_session: Session = None) -> Token:
        if not (access_token := configuration.connector.access_token):
            msg = "Missing auth token required for access token requests."
            logger.error(msg)
            logger.info("Use 'ACCESS_TOKEN' env variable to set it up.")
            raise TokenError(msg)

        logger.info(f"Requesting new token: {self.request_token_url}")
        async with aiohttp.ClientSession() as session:

            async with session.post(
                    self.request_token_url,
                    headers={"Bearer": access_token}
            ) as response:
                if response.status == 201:
                    response_data = await response.json()
                    return Token(
                        updated_at=datetime.utcnow(),
                        value=response_data.get("access_token"),
                    )
                if response.status == 400:
                    raise TokenError("Valid token already issued.")
                if response.status == 401:
                    raise TokenError(f"Invalid auth token: $ACCESS_TOKEN={access_token}")

                raise TokenError(f"Token request failed: {response.status}, {response.text}")

    def _query_token(self) -> Token | None:
        logger.info("Token not found in memory, querying the database.")
        with Session(engine) as session:
            token = session.query(TokenDb).filter_by(key=self.token_key).first()

        return Token(updated_at=token.updated_at, value=token.value) if token else None

    def _update_token(self, token: Token) -> Token:
        with Session(engine) as session:
            old_token = session.query(TokenDb).filter_by(key=self.token_key).first()
            if old_token:
                setattr(old_token, 'value', token.value)
                setattr(old_token, 'updated_at', token.updated_at)
            if not old_token:
                session.add(
                    TokenDb(key=self.token_key, value=token.value, updated_at=token.updated_at)
                )
            session.commit()
            return Token(updated_at=token.updated_at, value=token.value)

    @property
    def token_expired(self) -> bool:
        if not self._token:
            if stashed_token := self._query_token():
                self._token = stashed_token
            else:
                return True

        delta = (datetime.utcnow() - self._token.updated_at)
        if expired := delta > timedelta(seconds=configuration.connector.token_validity_secs):
            logger.info(f"Token from {self._token.updated_at!r} is now expired...")
        return expired

    async def get_token(self, force_refresh=False) -> Token:
        if force_refresh:
            logger.debug("Token refresh forced.")
            self._token = await self._refresh_token()

        if not self.token_expired:
            logger.debug(f"Token from {self._token.updated_at!r} is still valid...")
            return self._token

        new_token = self._update_token(await self._refresh_token())
        self._token = new_token
        return self._token
