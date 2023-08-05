from uuid import UUID

from pydantic import BaseModel


class Base(BaseModel):
    """Common parent."""
    id: UUID


class ProductBase(BaseModel):
    name: str
    description: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass
