import ssl

import pytest

from nea.services.server import Server


@pytest.fixture(scope='session')
def sample_msg_dict():
    return {
        "timestamp": "2020-05-27 11:42:01",
        "elapsed": 0.42,
        "status": 200,
        "pattern_ack": True
    }

@pytest.fixture(scope='session')
def sample_msg_str(sample_msg_dict):
    return json.dumps(sample_msg_dict)

@pytest.fixture(scope='session')
def ssl_context(sample_msg_dict):
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ssl_context.check_hostname = False
    ssl_context.load_verify_locations(Server.SERVER_CERT)
    return ssl_context
