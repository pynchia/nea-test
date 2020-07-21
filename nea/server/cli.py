"""
The command line interface to the Server application
"""

import asyncio
import click
import logging
from nea.server.main import main
import nea.services.server as server


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

@click.command()
@click.option(
    "--port", "-p", default=server.HOST_PORT, help="TCP Port on which to serve"
)
@click.option(
    "--cert", "-c", default=server.SERVER_CERT, type=click.Path(exists=True), help="TLS Certificate file"
)
@click.option(
    "--key", "-c", default=server.SERVER_KEY, type=click.Path(exists=True), help="TLS Key file"
)
@click.option(
    "--max-clients", "-m", default=server.MAX_CLIENTS, help="Max nummber of clients served concurrently"
)
@click.option(
    "--date-period", "-d", default=server.DATE_PERIOD, help="Time (sec.) between each date broadcast"
)
@click.option(
    "--verbose", "-v", is_flag=True, default=True, help="Log at debug level"
)
def cli(port, cert, key, max_clients, date_period, verbose):
    if verbose:
        log.setLevel(logging.DEBUG)
    asyncio.run(main(port, cert, key, max_clients, date_period))


if __name__ == '__main__':
    cli()
