import asyncio
from datetime import date
import logging
import ssl

from nea.services.message import MSG_SEPARATOR


log = logging.getLogger()

HOST_ADDR = 'localhost'
HOST_PORT = 3443
CLIENT_CERT = 'certs/my.crt'
CLIENT_KEY = 'certs/my.key'

class ServerDisconnect(Exception):
    pass


class Client:
    def __init__(self, processor,
                 host=HOST_ADDR, port=HOST_PORT,
                 cert=CLIENT_CERT, key=CLIENT_KEY):
        self.processor = processor
        self.host = host
        self.port = port
        self.ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.ssl_context.check_hostname = False
        self.ssl_context.load_verify_locations('certs/my.crt')

    async def __aenter__(self) -> None:
        self.reader, self.writer = await asyncio.open_connection(
            self.host, self.port, ssl=self.ssl_context)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> bool:
        self.writer.close()

    async def request_and_process(self, msg: str):
        self.writer.write((msg+MSG_SEPARATOR).encode())
        await self.writer.drain()
        log.info(f"sent {msg=}")
        response = (await self.reader.readline()).decode().rstrip()
        if not response:
            raise ServerDisconnect
        log.info(f"received {response=}")
        self.processor(response)  # process the response
