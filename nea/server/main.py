"""
The main module of the Server application
"""

import asyncio

from nea.services.server import Server
from nea.server.process import Processor


async def main(port: int, cert: str, key: str, max_clients:int, date_period: int):
    processor = Processor()
    async with Server(port, cert, key, max_clients, date_period, processor) as server:
        await server.server.serve_forever()
        # server.serve_forever() ??
