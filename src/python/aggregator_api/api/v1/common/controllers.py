import typing
from typing import Generic, TypeVar, Type, cast
from uuid import UUID

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from aggregator_api.api.v1.common import schemas
from aggregator_common import models
from aggregator_common.exceptions import NotFound, AggregatorError

C = TypeVar('C', bound=schemas.Base)
M = TypeVar('M', bound=models.Base)
U = TypeVar('U', bound=schemas.Base)


class SimpleController(Generic[C, M, U]):

    db_session: Session

    def __init__(self, db_session) -> None:
        self.db_session = db_session

    @property
    def create_schema(self) -> Type[C]:
        return typing.get_args(self.__orig_bases__[0])[0]

    @property
    def model(self) -> Type[M]:
        return typing.get_args(self.__orig_bases__[0])[1]

    @property
    def update_schema(self) -> Type[U]:
        return typing.get_args(self.__orig_bases__[0])[2]

    async def create(self, data: C, own_id: UUID = None) -> M:
        """Generic create method."""
        new_model = self.model(**data.model_dump())
        if own_id:
            setattr(new_model, 'id', str(own_id))
        try:
            self.db_session.add(new_model)
            self.db_session.commit()
        except Exception as exc_info:

            raise AggregatorError(
                f"Failed to create a new {self.model.__name__!r}, {exc_info}\n\n{data.model_dump()}"
            ) from exc_info
        return new_model

    async def get_all(self, use_paginate=False) -> Page[M] | list[M]:
        """Generic get all method."""
        if use_paginate:
            items = paginate(self.db_session, select(self.model))
        else:
            items = self.db_session.query(self.model).all()
        return items

    async def get_by_id(self, item_id: UUID) -> M:
        """Generic get by id method."""
        item = self.db_session.query(self.model).filter_by(id=str(item_id)).first()
        if not item:
            raise NotFound(self.model, 'id', item_id)
        return cast(M, item)

    async def update(self, item_id: UUID, data: U) -> M:
        """Generic update method."""
        updated_item = await self.get_by_id(item_id)
        for attr, value in data.model_dump().items():
            setattr(updated_item, attr, value)
        try:
            self.db_session.add(updated_item)
            self.db_session.commit()
        except Exception as exc_info:
            raise AggregatorError(
                f"Failed to update {self.model.__name__!r}, {exc_info}\n\n{data.model_dump()}"
            ) from exc_info
        return updated_item

    async def delete(self, product_id: UUID) -> None:
        self.db_session.delete(await self.get_by_id(product_id))
        self.db_session.commit()


class ProductsController(
    SimpleController[
        schemas.ProductCreate,
        models.Product,
        schemas.ProductUpdate
    ]
):
    """Simple controller for products CRUD"""
    pass


class OffersController(
    SimpleController[
        None,
        models.Offer,
        None
    ]
):
    """Simple controller for products CRUD"""

    async def create(self, data: C, own_id: UUID = None) -> M:
        raise AggregatorError('CREATE not allowed')

    async def update(self, item_id: UUID, data: U) -> M:
        raise AggregatorError('UPDATE not allowed')

    async def get_by_product(self, product_id: UUID, use_paginate: bool = False) -> list[M] | Page[M]:
        """Get all offers belonging to a particular product."""
        if use_paginate:
            items = paginate(self.db_session, select(self.model).filter_by(product_id=str(product_id)))
        else:
            items = self.db_session.query(self.model).filter_by(product_id=product_id).all()
        return items


