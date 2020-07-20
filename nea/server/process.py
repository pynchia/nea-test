"""
The functionality to process the incoming metrics
"""

# import json
import logging


# from nea.services.message import Message
from nea.services.message import MSG_SEPARATOR


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
        # it would be nice to wrap the msgs into a Message
        # try:
        #     message = Message.parse(msg)
        # except MessageDecodeError as e:
        #     log.error(e)
        # else:
        rev_msg = msg[::-1]
        # log.info(f"reversed msg {msg} to {rev_msg}")
        return rev_msg

