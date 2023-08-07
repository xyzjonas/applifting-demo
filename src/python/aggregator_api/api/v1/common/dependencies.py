from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from aggregator_api.api.v1.common.controllers import ProductsController, OffersController
from aggregator_api.auth import User, decode_token
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


async def client() -> RemoteClient:
    """Get the export tool."""
    return RemoteClient()


RemoteClientDependency = Annotated[RemoteClient, Depends(client)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
TokenDependency = Annotated[str, Depends(oauth2_scheme)]


async def logged_in(token: TokenDependency) -> User:
    """Get the export tool."""
    return decode_token(token)


LoggedInDependency = Annotated[User, Depends(logged_in)]
