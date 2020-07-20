import asyncio
from datetime import datetime
import logging
import ssl

from nea.services.message import MSG_SEPARATOR

log = logging.getLogger()


class Server:
    def __init__(self, port, cert, key, date_period, processor):
        self.port = port
        self.date_period = date_period
        self.processor = processor
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_context.check_hostname = False
        self.ssl_context.load_cert_chain(certfile=cert, keyfile=key)

        self.writers = {}

    def __enter__(self) -> None:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        pass

    async def _handle_client(self, reader, writer):
        # add the writer to the pool of open client connections
        self.writers[writer] = w_info = writer.get_extra_info('peername')
        log.info(f"Client {w_info} joins")
        while True:
            request = (await reader.readline()).decode().rstrip()
            if request:
                log.info(f"Received {request} from {w_info}")
                response = request[::-1]  # reverse the request
                writer.write((response+MSG_SEPARATOR).encode())
                log.info(f"Responded with {response} to {w_info}")
            else:  # I would have expected to be able to catch an exception
                log.info(f"Client {w_info} quits")
                break

        del self.writers[writer]  # remove the writer from the pool
        writer.close()
        await writer.wait_closed()

    async def start_server(self) -> None:
        """
        Start accepting connections from clients
        """
        await asyncio.start_server(
                self._handle_client,
                'localhost', self.port,
                ssl=self.ssl_context
        )
        print("Server is up")

    async def start_date_broadcast(self) -> None:
        """
        Start broadcasting date to clients
        """
        pass
        # loop.create_task(broadcast_date(DATE_SLEEP_PERIOD))
