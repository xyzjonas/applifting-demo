from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_serializer


class BaseUuid(BaseModel):
    id: UUID

    @field_serializer('id')
    def serialize_uuid(self, id_: UUID, _info):
        return str(id_)


class Offer(BaseUuid):
    price: int
    items_in_stock: int

    class Config:
        orm_mode = True


class Product(BaseUuid):
    name: str
    description: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    updated_at: datetime
    value: str
