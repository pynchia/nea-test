"""
The command line interface to the Server application
"""

import click
import logging
from nea.server.main import main


LISTEN_ADDR = 'localhost'
LISTEN_PORT = 3443
SERVER_CERT = 'certs/my.crt'
SERVER_KEY = 'certs/my.key'
DATE_PERIOD = 5

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

@click.command()
@click.option(
    "--port", "-p", default=LISTEN_PORT, help="TCP Port on which to serve"
)
@click.option(
    "--cert", "-c", default=SERVER_CERT, type=click.Path(exists=True), help="TLS Certificate file"
)
@click.option(
    "--key", "-c", default=SERVER_KEY, type=click.Path(exists=True), help="TLS Key file"
)
@click.option(
    "--date-period", "-d", default=DATE_PERIOD, help="Time (sec.) between each date broadcast"
)
@click.option(
    "--verbose", "-v", is_flag=True, default=True, help="Log at debug level"
)
def cli(port, cert, key, date_period, verbose):
    if verbose:
        log.setLevel(logging.DEBUG)
    main(port, cert, key, date_period)


if __name__ == '__main__':
    cli()
