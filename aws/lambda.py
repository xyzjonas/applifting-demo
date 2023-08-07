"""
Simple lambda function utilizing our watcher package. For sake of simplicity, everything here
gets built and bundled with dependencies in a single lambda layer.
"""
import json
import asyncio

from aggregator_watcher.watcher import Watcher


def lambda_handler(event, context):
    watcher = Watcher()
    print(watcher)
    asyncio.run(watcher.refresh())

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
