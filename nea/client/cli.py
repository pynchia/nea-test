"""
The command line interface to the client application
"""
import asyncio
import click
import logging

import nea.services.client as client
from nea.client.main import main



logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

@click.command()
@click.option(
    "--host", "-h", default=client.HOST_ADDR, help="The server's address"
)
@click.option(
    "--port", "-p", default=client.HOST_PORT, help="The server's TCP port"
)
@click.option(
    "--cert", "-c", default=client.CLIENT_CERT, type=click.Path(exists=True), help="TLS Certificate file"
)
@click.option(
    "--key", "-c", default=client.CLIENT_KEY, type=click.Path(exists=True), help="TLS Key file"
)
@click.option(
    "--verbose", "-v", is_flag=True, default=False, help="Log at debug level"
)
def cli(host, port, cert, key, verbose):
    if verbose:
        log.setLevel(logging.DEBUG)
    asyncio.run(main(host, port, cert, key))


if __name__ == '__main__':
    cli()
