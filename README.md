# Aggregator microservice
A simple FastAPI microservice API.

* **aggregator_api** - the API application itself
* **aggregator_connector** - the client connector for the remote service (register, query offers)
* **aggregator_watcher** - background task watching & updating products' offers

## Installation

#### 1) Local

```shell
poetry install
```
...afterwards:
```shell
# start the API server as a Python process using Uvicorn
applifting-demo
```
```shell
# start the watcher process - looping indefinitely
applifting-watcher
```

...and don't forget to set up these environment variables:
```shell
export ACCESS_TOKEN=<your-token-here>
export DATABASE_URI=<your-database-connection-string-here>
export CLOUD_URI=<remote-service-base-url-here>
```

#### 2) Docker & Compose
Run individual images/services
```shell
# 1) API
docker run -it --rm --entrypoint applifting-demo scotch3840/misc:applifting-demo
# 2) Watcher
docker run -it --rm --entrypoint applifting-watcher scotch3840/misc:applifting-demo
```
...or use attached compose file.
```shell
docker compose up -d
```
```shell
# ACCESS_TOKEN is the only required variable
export ACCESS_TOKEN=<your-token-here>
```
