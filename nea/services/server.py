import asyncio
from datetime import date
import logging
import ssl

from nea.services.message import MSG_SEPARATOR


log = logging.getLogger()

HOST_ADDR = 'localhost'
HOST_PORT = 3443
SERVER_CERT = 'certs/my.crt'
SERVER_KEY = 'certs/my.key'
MAX_CLIENTS = 100  # max number of contemporary clients served
DATE_PERIOD = 10  # seconds between date broadcasts to the clients

class Server:
    def __init__(self,
                 processor,
                 port=HOST_PORT,
                 cert=SERVER_CERT, key=SERVER_KEY,
                 max_clients=MAX_CLIENTS,
                 date_period=DATE_PERIOD):
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
        log.info("Server has shutdown")

    async def _handle_client(self, reader, writer):
        w_info = writer.get_extra_info('peername')
        if len(self.writers) >= self.max_clients:
            log.warning(f"Refusing {w_info} to join, too many clients (max {self.max_clients}), disconnected")
            writer.close()
            try:
                await writer.wait_closed()
            except ssl.SSLError:
                pass
            return

        # add the writer to the pool of open client connections
        self.writers[writer] = w_info
        log.info(f"client {w_info} joins")
        while True:
            request = (await reader.readline()).decode().rstrip()
            if request:
                log.info(f"{request=} from {w_info}")
                response = self.processor(request)  # process the request
                writer.write((response+MSG_SEPARATOR).encode())
                log.info(f"{response=} sent to {w_info}")
            else:  # I would have expected to be able to catch an exception
                log.info(f"client {w_info} quits")
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
                HOST_ADDR, self.port,
                ssl=self.ssl_context
        )
        log.info("server is up")

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
                log.info(f"{cur_date=} sent to {w_info}")

    async def _start_broadcaster(self) -> None:
        """
        Start broadcasting date to all clients
        """
        self.broadcaster = asyncio.create_task(self._broadcast_date())
        log.info("date-broadcaster is up")
