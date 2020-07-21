
import asyncio
from datetime import date
import pytest
import ssl

from nea.server.process import Processor
from nea.services.client import Client, ServerDisconnect
from nea.services.server import Server
from nea.services.message import MSG_SEPARATOR



@pytest.mark.asyncio
async def test_client_req_and_response(ssl_context):
    msg = "hello"

    class TstServer(Server):
        """
        A server that accepts one request and sends one response
        """
        async def _handle_client(self, reader, writer):
            request = (await reader.readline()).decode().rstrip()
            assert request == msg
            response = self.processor(request)  # process the request
            writer.write((response+MSG_SEPARATOR).encode())

    async with TstServer(Processor()) as server:
        async with Client() as client:
            response = await client.request(msg)
            assert response == msg[::-1]


@pytest.mark.asyncio
async def test_client_reaction_to_srv_disconnect(ssl_context):
    msg = "hello"

    class TstServer(Server):
        """
        A server that accepts one client only
        """
        num_clients = 0
        async def _handle_client(self, reader, writer):
            TstServer.num_clients += 1
            if TstServer.num_clients > 1:
                writer.close()
                return

    async with TstServer(Processor()) as server:
        async with Client() as client_ok, Client() as client_ko:
            with pytest.raises(ServerDisconnect):
                response = await client_ko.request(msg)
