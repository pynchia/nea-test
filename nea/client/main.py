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
    async with Client(host, port, cert, key) as client:
        async for msg in generate_data():
            try:
                response = await client.request(msg)
            except ServerDisconnect:
                log.error("Server has disconnected")
                break
