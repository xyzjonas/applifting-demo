from uuid import UUID

from pydantic import BaseModel


class Base(BaseModel):
    """Common parent."""
    id: UUID


class ProductBase(BaseModel):
    name: str
    description: str


class ProductRead(ProductBase):
    id: UUID

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class GetPutPostOffer(Base):
    price: int
    items_in_stock: int
