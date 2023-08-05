import os
from functools import lru_cache

from pydantic import validator, field_validator
from pydantic_settings import BaseSettings

from datetime import datetime


now = datetime.now().timestamp()


class DefaultConfiguration(BaseSettings):
    database_uri: str
    debug_mode: bool = False

    access_token: str | None = None
    cloud_uri: str = "https://python.exercise.applifting.cz/"
    token_validity_secs: int = 5 * 60

    uvicorn_host: str = "0.0.0.0"
    uvicorn_port: int = 8000

    allowed_cors_origins: str = "http://localhost:5173"


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

