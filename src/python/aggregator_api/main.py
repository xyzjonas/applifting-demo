import uvicorn
from loguru import logger

from aggregator_api.app import app
from aggregator_common.configuration import get_configuration
from aggregator_common.models import create_all


def serve():
    options = "\n".join([f"{k.upper()}: '{v}'" for k, v in get_configuration()])
    logger.info(f"""
Starting Aggregator API

Configuration:
------------------
{options}
""")

    create_all()

    uvicorn.run(
        app,
        host=get_configuration().uvicorn_host,
        port=get_configuration().uvicorn_port
    )


if __name__ == '__main__':
    serve()
