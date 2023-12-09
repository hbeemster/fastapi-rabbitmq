import pytest
from fastapi.testclient import TestClient

from fastapi_rabbitmq.config import config
from fastapi_rabbitmq.constants import PROCESS_URL
from fastapi_rabbitmq.messages import Job


# ------------------------------------------------------------------------
@pytest.fixture(scope="function")
def client_with_one_consumer():
    """This fixture will start the app."""
    from fastapi_rabbitmq.app import app

    with TestClient(app) as client:
        yield client

# ------------------------------------------------------------------------
@pytest.fixture(scope="function")
def client_with_three_consumers():
    """This fixture will start the app."""
    from fastapi_rabbitmq.app import app

    config.number_of_consumers = 3
    with TestClient(app) as client:
        yield client


# ------------------------------------------------------------------------
@pytest.fixture
def job():
    """"""
    data = {"name": "TADA", "duration": 3.0}
    return Job(**data)

# ------------------------------------------------------------------------
@pytest.fixture
def jobs(job):
    """"""
    jobs = []
    for duration in range(1, 4):
        data = {"name": "TADA", "duration": duration}
        job = Job(**data)
        jobs.append(job)
    return jobs

# ------------------------------------------------------------------------
@pytest.fixture
def process_url():
    """"""
    return PROCESS_URL
