import uuid
from datetime import datetime
from typing import List

from sqlalchemy import String, Integer, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from aggregator_common import configuration

engine = create_engine(configuration.api.database_uri, echo=configuration.api.debug_mode)


def create_all():
    Base.metadata.create_all(engine)


def drop_all():
    Base.metadata.drop_all(engine)


def uuid_factory():
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    # Let's not use UUID as the primary key, so that we can use sqlite for testing.
    key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Product(Base):
    """Product db ORM."""
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(unique=True, default=uuid_factory)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)

    offers: Mapped[List['Offer']] = relationship(back_populates="product", cascade="all,delete")


class Offer(Base):
    """Offer db ORM."""
    __tablename__ = "offers"

    id: Mapped[str] = mapped_column(unique=True, default=uuid_factory)
    price: Mapped[int] = mapped_column(Integer)
    items_in_stock: Mapped[int] = mapped_column(Integer)

    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"))
    product: Mapped[Product] = relationship(back_populates="offers")


class Token(Base):
    """Token db ORM.

    We're considering a distributed deployment method for this application, where
    we only use a single access token. To efficiently manage and reuse
    this access token within its validity period, we're planning to keep
    it safely in a shared database.
    """
    __tablename__ = "token"

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    value: Mapped[str] = mapped_column(String, nullable=False)
