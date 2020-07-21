# import json
import ssl

import pytest

import nea.services.server as server


# @pytest.fixture(scope='session')
# def sample_text_msg_dict():
#     return {
#         "msg_type": "string",
#         "payload": "hello"
#     }

# @pytest.fixture(scope='session')
# def sample_date_msg_dict():
#     return {
#         "msg_type": "date",
#         "payload": "2020-07-20"
#     }

# @pytest.fixture(scope='session')
# def sample_text_msg_str(sample_text_msg_dict):
#     return json.dumps(sample_text_msg_dict)

# @pytest.fixture(scope='session')
# def sample_date_msg_str(sample_date_msg_dict):
#     return json.dumps(sample_date_msg_dict)

@pytest.fixture(scope='session')
def ssl_context():
    # this fixture is now used for both the client and the server
    # but in principle two separate contexts would be needed
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ssl_context.check_hostname = False
    ssl_context.load_verify_locations(server.SERVER_CERT)
    return ssl_context
