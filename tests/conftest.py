import pytest
from fastapi.testclient import TestClient


# ------------------------------------------------------------------------
@pytest.fixture(scope="session")
def client():
    """This fixture will start the app."""
    from fastapi_rabbitmq.app import app

    with TestClient(app) as client:
        yield client
