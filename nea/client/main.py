"""
The main module of the client application
"""

import asyncio
import logging

from nea.services.client import Client, ServerDisconnect
from nea.client.generate import generate_data
# from nea.client.process import Processor


log = logging.getLogger()


async def main(host: str, port: int, cert: str, key: str):
    processor = lambda resp: log.info(f"processing {resp}")
    async with Client(host, port, cert, key, processor) as client:
        async for msg in generate_data():
            try:
                await client.request_and_process(msg)
            except ServerDisconnect:
                log.error("Server has disconnected")
                break
