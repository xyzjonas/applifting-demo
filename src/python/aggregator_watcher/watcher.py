import asyncio
import uuid
from datetime import timedelta
from uuid import UUID

from loguru import logger
from sqlalchemy import update, delete, select, column, insert
from sqlalchemy.orm import Session

from aggregator_common.models import engine
from aggregator_common.models import Product as ProductDb
from aggregator_common.models import Offer as OfferDb
from aggregator_common.schemas import Offer
from aggregator_connector.client import RemoteClient
from aggregator_common import configuration


class Watcher:
    """Simple product watcher, that updates offers."""

    client: RemoteClient
    sleep_secs: int

    def __init__(self, sleep_secs: int = configuration.watcher.sleep_secs) -> None:
        self.client = RemoteClient()
        self.sleep_secs = sleep_secs

    async def _query_product_offers(self, product_id: UUID) -> tuple[UUID, list[Offer]]:
        logger.debug(f"Querying product {product_id!r}.")
        try:
            prod_offers = await self.client.get_offers(product_id=product_id)
        except Exception as exc:
            logger.exception("Query failed.")
            logger.error(f"Querying product {product_id!r} FAILED, ignoring this product's offers.")
            return uuid.uuid4(), []
        logger.debug(f"Querying product {product_id!r}, got {len(prod_offers)} offers.")
        return product_id, prod_offers

    @staticmethod
    def _get_update_offer_statement(product_id: UUID, new_offer: Offer):
        """Update existing offers."""
        return (
            update(OfferDb)
            .where(OfferDb.id.in_([str(new_offer.id)]))
            .where(OfferDb.product_id.in_([str(product_id)]))
            .values(
                product_id=str(product_id),
                price=new_offer.price,
                items_in_stock=new_offer.items_in_stock,
            )
        )

    @staticmethod
    def _get_insert_offer_statement(product_id: UUID, offer: Offer):
        """Insert new offers."""
        return (
            insert(OfferDb)
            .values(
                id=str(offer.id),
                product_id=str(product_id),
                price=offer.price,
                items_in_stock=offer.items_in_stock
            )
        )

    @staticmethod
    def _get_delete_offers_statement(except_offers: list[Offer]):
        """Delete all expired offers."""
        return (
            delete(OfferDb)
            .where(OfferDb.id.notin_([str(ofr.id) for ofr in except_offers]))
        )

    async def refresh(self):
        """Update all offers with actual remote data."""
        with Session(engine) as session:
            all_products = session.query(ProductDb).all()
            logger.info(f"Updating all {len(all_products)} products.")

        tasks = []
        for product in all_products:
            tasks.append(self._query_product_offers(product.id))

        with Session(engine) as session:

            sql_statements = []
            do_not_delete = []
            old_offers_ids = [o_id for _, o_id in session.execute(select(OfferDb, column('id')))]
            logger.info(old_offers_ids)
            for prod_id, new_offers in await asyncio.gather(*tasks):
                for new_offer in new_offers:
                    do_not_delete.append(new_offer)
                    if str(new_offer.id) not in old_offers_ids:
                        sql_statements.append(self._get_insert_offer_statement(prod_id, new_offer))
                    else:
                        sql_statements.append(self._get_update_offer_statement(prod_id, new_offer))

            sql_statements.append(self._get_delete_offers_statement(except_offers=do_not_delete))
            for stmt in sql_statements:
                logger.debug(f"Executing: {stmt}")
                session.execute(stmt)

            session.commit()

    async def loop(self):
        """Main watcher process loop."""
        logger.info("Starting loop.")
        while True:
            try:
                await self.refresh()
            except Exception as exc_info:
                logger.exception("Error while looping...")
                await asyncio.sleep(5)
            else:
                logger.debug(f"Loop done, sleeping {self.sleep_secs}s")
                await asyncio.sleep(self.sleep_secs)
