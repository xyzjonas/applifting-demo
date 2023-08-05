from aggregator_common.models import Product, Offer


def test_delete_orphan(db_session, product, offers):
    p = db_session.query(Product).first()
    assert len(p.offers) == len(offers)

    db_session.delete(p)
    db_session.commit()

    p = db_session.query(Product).first()
    assert p is None
    remaining_offers = db_session.query(Offer).all()
    assert len(remaining_offers) == 0
