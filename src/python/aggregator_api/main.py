import uvicorn
from loguru import logger

from aggregator_api.app import app
from aggregator_common import configuration
from aggregator_common.models import create_all


def serve():
    options = "\n".join([f"{k.upper()}: '{v}'" for k, v in configuration.api])
    logger.info(f"""
Starting Aggregator API

Configuration:
------------------
{options}
""")
    create_all()
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == '__main__':
    serve()
