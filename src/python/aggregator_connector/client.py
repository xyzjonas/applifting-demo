import posixpath
from uuid import UUID

import aiohttp
from aiohttp import ClientResponseError
from loguru import logger
from pydantic import ValidationError, BaseModel

from aggregator_common import configuration
from aggregator_common.exceptions import AggregatorError, RemoteConnectionError
from aggregator_common.schemas import Offer, Product
from aggregator_connector.token import TokenManager


class RegisterProductResponse(BaseModel):
    id: UUID


class RemoteClient:

    token_manager: TokenManager
    base_uri: str = posixpath.join(configuration.connector.cloud_uri, "api/v1/products")

    def __init__(self) -> None:
        self.token_manager = TokenManager()

    @staticmethod
    def wrap_request(coro):
        retries = 1
        max_retries = 3

        async def inner(*args, **kwargs):
            try:
                return await coro(*args, **kwargs)
            except ClientResponseError as exc_info:
                if exc_info.status >= 400:
                    nonlocal retries
                    if retries <= max_retries:
                        logger.warning(f"Got {exc_info.status}, retrying {retries}/{max_retries}")
                        retries += 1
                        return await inner(*args, **kwargs)
                raise RemoteConnectionError(
                    f"Aggregator connector request failed with: {exc_info.status}"
                ) from exc_info
            except ValidationError as exc_info:
                raise RemoteConnectionError(
                    f"Unexpected response from remote service", exc_info
                ) from exc_info
            except Exception as exc_info:
                logger.exception("Unexpected error while executing API request.")
                raise RemoteConnectionError(str(exc_info)) from exc_info

        return inner

    @wrap_request
    async def register_product(self, product: Product) -> Product:
        async with aiohttp.ClientSession() as session:
            url = posixpath.join(self.base_uri, "register")
            logger.info(f"Registering a new product {product.id!r}: {url!r}")
            async with session.post(
                    url,
                    headers={
                      'Bearer': (await self.token_manager.get_token()).value
                    },
                    json=product.model_dump(),
            ) as response:
                response.raise_for_status()
                response = RegisterProductResponse(**await response.json())
        if response.id != product.id:
            msg = f"Unexpected response from remote service: {response.id} != {product.id}"
            logger.error(msg)
            raise AggregatorError(msg)
        return product

    @wrap_request
    async def get_offers(self, product_id: UUID) -> list[Offer]:
        async with aiohttp.ClientSession() as session:
            url = posixpath.join(self.base_uri, str(product_id), "offers")
            logger.info(f"Querying product offers {product_id!r}: {url!r}")
            async with session.get(
                url,
                headers={
                    'Bearer': (await self.token_manager.get_token()).value
                },
            ) as response:
                response.raise_for_status()
                offers = await response.json()

        return [Offer(**offer) for offer in offers]
