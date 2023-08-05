from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from aggregator_api.api.v1.common.controllers import ProductsController
from aggregator_api.configuration import get_configuration


async def db_session() -> Session:
    """Get the export tool."""
    engine = create_engine(get_configuration().database_uri, echo=get_configuration().debug_mode)
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

