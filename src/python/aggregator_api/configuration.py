import os
from functools import lru_cache

from pydantic_settings import BaseSettings

from datetime import datetime


now = datetime.now().timestamp()


class DefaultConfiguration(BaseSettings):
    database_uri: str
    debug_mode: bool = False


class DevelConfiguration(DefaultConfiguration):
    database_uri: str = f"sqlite:////tmp/app-db-{now}.sqlite"
    debug_mode: bool = True


class TestConfiguration(DevelConfiguration):
    pass


@lru_cache
def get_configuration():
    match(os.getenv("APP_MODE")):
        case ["dev", "development"]:
            return DevelConfiguration()
        case ["prod", "production"]:
            return DefaultConfiguration()
        case _:
            return TestConfiguration()

