from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from aggregator_api.api.v1.common.controllers import ProductsController, OffersController
from aggregator_common.models import engine
from aggregator_connector.client import RemoteClient


async def db_session() -> Session:
    """Get the export tool."""
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


DbSessionDependency = Annotated[Session, Depends(db_session)]


async def products(db: DbSessionDependency) -> ProductsController:
    """Get the export tool."""
    return ProductsController(db)


ProductsDependency = Annotated[ProductsController, Depends(products)]


async def offers(db: DbSessionDependency) -> OffersController:
    """Get the export tool."""
    return OffersController(db)


OffersDependency = Annotated[OffersController, Depends(offers)]


async def client(db: DbSessionDependency) -> RemoteClient:
    """Get the export tool."""
    return RemoteClient()


AggregatorClientDependency = Annotated[RemoteClient, Depends(client)]

