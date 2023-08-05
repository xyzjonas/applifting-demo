from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Offer(BaseModel):
    id: UUID
    price: int
    items_in_stock: int

    class Config:
        orm_mode = True


class Product(BaseModel):
    id: UUID
    name: str
    description: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    updated_at: datetime
    value: str
