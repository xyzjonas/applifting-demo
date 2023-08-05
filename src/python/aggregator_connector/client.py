import asyncio
import posixpath
import uuid
from uuid import UUID

import aiohttp
from aiohttp import ClientResponseError
from loguru import logger
from sqlalchemy.orm import Session

from aggregator_common.configuration import get_configuration
from aggregator_common.exceptions import AggregatorError
from aggregator_connector.token import TokenManager


class AggregatorClient:

    token_manager: TokenManager
    base_uri: str = posixpath.join(get_configuration().cloud_uri, "/api/v1/products")

    db_session: Session | None

    def __init__(self, session: Session = None) -> None:
        self.token_manager = TokenManager()
        self.db_session = session

    @staticmethod
    def wrap_request(coro):

        async def inner(*args, **kwargs):
            try:
                return await coro(*args, **kwargs)
            except ClientResponseError as exc_info:
                raise AggregatorError(
                    f"Aggregator connector request failed with: {exc_info.status}", exc_info
                ) from exc_info
            except Exception as exc_info:
                logger.exception("Unexpected error while executing API request.")
                raise AggregatorError(str(exc_info)) from exc_info

        return inner

    @wrap_request
    async def register_product(self, product_id: UUID, product_name: str, product_description: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    posixpath.join(self.base_uri, "register"),
                    headers={
                      'Bearer': await self.token_manager.get_token()
                    },
                    data={
                        'id': product_id,
                        'name': product_name,
                        'description': product_description,
                    },
            ) as response:
                response.raise_for_status()
        x  = await response.json()
        return x


    async def get_offers(self, product_id: UUID) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                posixpath.join(self.base_uri, str(product_id), "offers"),
                headers={
                    'Bearer': await self.token_manager.get_token()
                },
            ) as response:
                response.raise_for_status()
                offers = await response.json()

        return offers


async def main():
    from aggregator_common.models import create_all
    options = "\n".join([f"{k.upper()}: '{v}'" for k, v in get_configuration()])
    logger.info(f"""
    {options}
    """)
    create_all()
    client = AggregatorClient()
    x = await client.get_offers(uuid.uuid4())
    y = 12


if __name__ == '__main__':
    asyncio.run(main())
