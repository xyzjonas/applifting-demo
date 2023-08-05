import uuid

from sqlalchemy import String, Integer, create_engine, Engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from aggregator_api.configuration import get_configuration


engine = create_engine(get_configuration().database_uri, echo=get_configuration().debug_mode)


def create_all():
    Base.metadata.create_all(engine)


def drop_all():
    Base.metadata.drop_all(engine)


def uuid_factory():
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    # Let's not use UUID as the primary key, so that we can use sqlite for testing.
    key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id: Mapped[str] = mapped_column(unique=True, default=uuid_factory)


class Product(Base):
    """Product db ORM."""
    __tablename__ = "products"

    name = mapped_column(String)
    description = mapped_column(String)


class Offer(Base):
    """Offer db ORM."""
    __tablename__ = "offers"

    price = mapped_column(Integer)
    items_in_stock = mapped_column(Integer)
