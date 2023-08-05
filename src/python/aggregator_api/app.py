from loguru import logger
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from aggregator_api.api import router
from aggregator_api.error_handlers import register_exception_handlers
from aggregator_common.configuration import get_configuration

app = FastAPI()
app.include_router(router)

for origin in get_configuration().allowed_cors_origins.split(","):
    logger.info(f"Allow CORS from origin {origin!r}.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_configuration().allowed_cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
