import uuid

from aggregator_common.models import Offer as OfferDb
from aggregator_common.models import Product as ProductDb
from aggregator_common.schemas import Offer

from aggregator_watcher.watcher import Watcher


def test_update_statement(db_session, product, random_str):
    offer_id = uuid.uuid4()
    db_session.add(
        OfferDb(
            product_id=product.id,
            id=str(offer_id),
            items_in_stock=5,
            price=1,
        )
    )
    db_session.commit()

    new_offer = Offer(id=offer_id, items_in_stock=50, price=10)
    stmt = Watcher._get_update_offer_statement(product.id, new_offer)
    db_session.execute(stmt)
    db_session.commit()

    p = db_session.query(ProductDb).first()
    assert len(p.offers) == 1
    ofr = p.offers[0]
    assert ofr.items_in_stock == 50


def test_delete_statement(db_session, offers):
    db_session.add(OfferDb(id=str(uuid.uuid4()), items_in_stock=99, price=9, product_id="asd"))
    db_session.commit()

    ofrs = db_session.query(OfferDb).all()
    assert len(ofrs) == len(offers) + 1

    offers_pydantic = [Offer(
        id=ofr.id,
        items_in_stock=ofr.items_in_stock,
        price=ofr.price,
    ) for ofr in offers]

    stmt = Watcher._get_delete_offers_statement(except_offers=offers_pydantic)
    db_session.execute(stmt)
    db_session.commit()

    ofrs = db_session.query(OfferDb).all()
    assert len(ofrs) == len(offers)
