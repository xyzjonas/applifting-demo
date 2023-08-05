from fastapi import FastAPI

from aggregator_api.api import router
from aggregator_api.error_handlers import register_exception_handlers
from aggregator_api.models import create_all

app = FastAPI()
app.include_router(router)

register_exception_handlers(app)

create_all()


if __name__ == '__main__':
    pass
