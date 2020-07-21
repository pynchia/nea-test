"""
The main module of the server application
"""

import asyncio

from nea.services.server import Server
from nea.server.process import Processor


async def main(port: int, cert: str, key: str, max_clients:int, date_period: int):
    processor = Processor()  # processes the requests
    async with Server(processor, port, cert, key, max_clients, date_period) as server:
        await server.server.serve_forever()
