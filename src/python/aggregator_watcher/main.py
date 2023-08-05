import asyncio

from loguru import logger

from aggregator_common.models import create_all
from aggregator_common import configuration
from aggregator_watcher.watcher import Watcher


def start_watch():
    options = "\n".join([f"{k.upper()}: '{v}'" for k, v in configuration.watcher])
    logger.info(f"""
Starting Watcher

Configuration:
------------------
{options}
""")
    watcher = Watcher()
    create_all()
    asyncio.run(watcher.loop())


if __name__ == '__main__':
    start_watch()
