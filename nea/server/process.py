"""
The functionality to process the incoming metrics
"""

from datetime import datetime
import json
import logging

import psycopg2 as pg

from aiven.broker.services.message import Message


log = logging.getLogger()


class MessageDecodeError(Exception):
    pass


class Processor:
    """
    Process the incoming messages from the client, i.e.
    Reverse the string
    """

    def __init__(self):
        pass

    def __call__(self, msg: str):
        """
        Process the incoming msg
        """
        rev_msg = msg[::-1]
        log.info(f"Reversed msg {msg} to {rev_msg}")
        return rev_msg

        # try:
        #     message = Message.parse(msg)
        # except MessageDecodeError as e:
        #     log.error(e)
        # else:
