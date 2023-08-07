from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from aggregator_api.api import router
from aggregator_api.auth import login
from aggregator_api.error_handlers import register_exception_handlers
from aggregator_common import configuration

app = FastAPI()

app.include_router(router)

register_exception_handlers(app)

for origin in configuration.api.allowed_cors_origins.split(","):
    logger.info(f"Allow CORS from origin {origin!r}.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=configuration.api.allowed_cors_origins.split(","),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/token")
def api_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return {"access_token": login(form_data.username, form_data.password), "token_type": "bearer"}
