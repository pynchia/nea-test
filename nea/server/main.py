"""
The main module of the Server application
"""

import asyncio

from nea.services.message import MSG_SEPARATOR
from nea.services.server import Server
from nea.server.process import Processor


def main(port: int, cert: str, key: str, date_period: int):
    processor = Processor()
    with Server(port, cert, key, date_period, processor) as server:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(server.start_server())
        loop.run_forever()
