
import asyncio
from datetime import date
import pytest
import ssl

from nea.server.process import Processor
from nea.services.server import Server
from nea.services.message import MSG_SEPARATOR


@pytest.mark.asyncio
async def test_server_end_to_end_without_date_received_yet(ssl_context):
    async with Server(
        Server.HOST_PORT,
        Server.SERVER_CERT, Server.SERVER_KEY,
        Server.MAX_CLIENTS, Server.DATE_PERIOD,
        Processor()
        ) as server:

        reader, writer = await asyncio.open_connection(
            Server.HOST_ADDR, Server.HOST_PORT, ssl=ssl_context
        )
        request = 'test'
        writer.write((request+MSG_SEPARATOR).encode())
        # await writer.drain()
        response = (await reader.readline()).decode().rstrip()
        assert request == response[::-1]
        writer.close()
        await writer.wait_closed()

@pytest.mark.asyncio
async def test_server_end_to_end_receive_date_only(ssl_context):
    async with Server(
        Server.HOST_PORT,
        Server.SERVER_CERT, Server.SERVER_KEY,
        Server.MAX_CLIENTS, Server.DATE_PERIOD,
        Processor()
        ) as server:

        reader, writer = await asyncio.open_connection(
            Server.HOST_ADDR, Server.HOST_PORT, ssl=ssl_context
        )

        await asyncio.sleep(server.DATE_PERIOD+1)

        broadcast_date = (await reader.readline()).decode().rstrip()
        cur_date = str(date.today())
        assert broadcast_date == cur_date

        writer.close()
        await writer.wait_closed()


@pytest.mark.asyncio
async def test_server_end_to_end_with_all(ssl_context):
    async with Server(
        Server.HOST_PORT,
        Server.SERVER_CERT, Server.SERVER_KEY,
        Server.MAX_CLIENTS, Server.DATE_PERIOD,
        Processor()
        ) as server:

        reader, writer = await asyncio.open_connection(
            Server.HOST_ADDR, Server.HOST_PORT, ssl=ssl_context
        )
        request = 'test'
        writer.write((request+MSG_SEPARATOR).encode())
        # await writer.drain()
        response = (await reader.readline()).decode().rstrip()
        assert request == response[::-1]

        await asyncio.sleep(server.DATE_PERIOD+1)

        broadcast_date = (await reader.readline()).decode().rstrip()
        cur_date = str(date.today())
        assert broadcast_date == cur_date

        writer.close()
        await writer.wait_closed()

@pytest.mark.asyncio
async def test_server_too_many_clients(ssl_context):
    async with Server(
        Server.HOST_PORT,
        Server.SERVER_CERT, Server.SERVER_KEY,
        Server.MAX_CLIENTS, Server.DATE_PERIOD,
        Processor()
        ) as server:

        # saturate the server connecting the max supported clients
        cnx = [
            await asyncio.open_connection(
                Server.HOST_ADDR, Server.HOST_PORT, ssl=ssl_context
            ) for _ in range(Server.MAX_CLIENTS)
        ]

        # One more client should fail
        reader, writer = await asyncio.open_connection(
            Server.HOST_ADDR, Server.HOST_PORT, ssl=ssl_context
        )
        request = 'test'
        writer.write((request+MSG_SEPARATOR).encode())
        # await writer.drain()
        response = (await reader.readline()).decode().rstrip()
        assert not response # expect no response

        writer.close()
        await writer.wait_closed()

        # disconnect all initial max clients
        for reader, writer in cnx:
            writer.close()
            await writer.wait_closed()
