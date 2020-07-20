
from nea.services.message import Message
from nea.services.message import Message


async def generate_data():
    """
    Generate the input data to be sent to the server
    """
    while True:
        try:
            data = input('Please enter a string >> ')
        except KeyboardInterrupt:
            break
        if data:
            yield data
