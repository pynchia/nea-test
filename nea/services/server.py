import asyncio
from datetime import date
import logging
import ssl

from nea.services.message import MSG_SEPARATOR


log = logging.getLogger()

class Server:
    HOST_ADDR = 'localhost'
    HOST_PORT = 3443
    SERVER_CERT = 'certs/my.crt'
    SERVER_KEY = 'certs/my.key'
    MAX_CLIENTS = 2
    DATE_PERIOD = 5

    def __init__(self, port, cert, key, max_clients, date_period, processor):
        self.port = port
        self.max_clients = max_clients
        self.date_period = date_period
        self.processor = processor
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_context.check_hostname = False
        self.ssl_context.load_cert_chain(certfile=cert, keyfile=key)

        self.writers = {}

    async def __aenter__(self) -> None:
        await self._start_server()
        await self._start_broadcaster()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> bool:
        self.broadcaster.cancel()
        self.server.close()
        await self.server.wait_closed()

    async def _handle_client(self, reader, writer):
        # add the writer to the pool of open client connections
        self.writers[writer] = w_info = writer.get_extra_info('peername')
        log.info(f"Client {w_info} joins")
        while True:
            request = (await reader.readline()).decode().rstrip()
            if request:
                log.info(f"Received {request} from {w_info}")
                response = self.processor(request)  # process the request
                writer.write((response+MSG_SEPARATOR).encode())
                log.info(f"Responded with {response} to {w_info}")
            else:  # I would have expected to be able to catch an exception
                log.info(f"Client {w_info} quits")
                break

        del self.writers[writer]  # remove the writer from the pool
        writer.close()
        await writer.wait_closed()

    async def _start_server(self) -> None:
        """
        Start accepting connections from clients
        """
        self.server = await asyncio.start_server(
                self._handle_client,
                self.HOST_ADDR, self.port,
                ssl=self.ssl_context
        )
        log.info("Server is up")

    async def _broadcast_date(self):
        while True:
            try:
                await asyncio.sleep(self.date_period)
            except asyncio.CancelledError:
                log.info("Cancelling ")
                # insert cleanup here if needed
                raise
            cur_date = str(date.today())
            for writer, w_info in self.writers.items():
                writer.write((cur_date+MSG_SEPARATOR).encode())
                log.info(f"Written {cur_date} to {w_info}")

    async def _start_broadcaster(self) -> None:
        """
        Start broadcasting date to all clients
        """
        self.broadcaster = asyncio.create_task(self._broadcast_date())
