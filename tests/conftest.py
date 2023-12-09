import pytest
from fastapi.testclient import TestClient

from fastapi_rabbitmq.config import config
from fastapi_rabbitmq.messages import Task


# ------------------------------------------------------------------------
@pytest.fixture(scope="session")
def client_with_one_consumer():
    """This fixture will start the app."""
    from fastapi_rabbitmq.app import app

    with TestClient(app) as client:
        yield client

# ------------------------------------------------------------------------
@pytest.fixture(scope="session")
def client_with_three_consumers():
    """This fixture will start the app."""
    from fastapi_rabbitmq.app import app

    config.number_of_consumers = 3
    with TestClient(app) as client:
        yield client


# ------------------------------------------------------------------------
@pytest.fixture
def tasks():
    """"""
    tasks = []
    for duration in range(1, 4):
        data = {"name": "TADA", "duration": duration}
        task = Task(**data)
        tasks.append(task)
    return tasks
