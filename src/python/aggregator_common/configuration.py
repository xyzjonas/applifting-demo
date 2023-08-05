from pydantic_settings import BaseSettings


class DatabaseConfiguration(BaseSettings):
    database_uri: str = f"sqlite:////tmp/applifting-tmp-db.sqlite"
    debug_mode: bool = False


class RemoteConfiguraton(BaseSettings):
    access_token: str | None = None
    # cloud_uri: str = "https://python.exercise.applifting.cz/"
    cloud_uri: str = "http://localhost:9000/"
    token_validity_secs: int = 5 * 60


class ApiConfiguration(DatabaseConfiguration, RemoteConfiguraton):
    allowed_cors_origins: str = "http://localhost:5173"


class ConnectorConfiguration(DatabaseConfiguration, RemoteConfiguraton):
    pass


class WatcherConfiguration(DatabaseConfiguration, RemoteConfiguraton):
    sleep_secs: int = 10


watcher = WatcherConfiguration()
connector = ConnectorConfiguration()
api = ApiConfiguration()

