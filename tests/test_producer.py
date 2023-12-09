import logging
from time import sleep
from typing import List

from _pytest.logging import LogCaptureFixture

from fastapi_rabbitmq.logger import logger
from fastapi_rabbitmq.messages import Job


# ------------------------------------------------------------------------
def send_jobs(client, process_url: str, jobs: List[Job]) -> None:
    """Send all jobs to the rabbitmq."""
    for job in jobs:
        client.post(process_url, data=job.model_dump_json())


# ------------------------------------------------------------------------
def wait_until_ready(caplog: LogCaptureFixture, jobs: List[Job]) -> None:
    """Watch the log for the correlation_ids."""
    match = {f"Job with correlation_id: {job.correlation_id} done!!!" for job in jobs}
    while not set(caplog.messages).issuperset(match):
        logger.debug("waiting...")
        sleep(1)


# ------------------------------------------------------------------------
def test_send_single_job(client_with_one_consumer, job, process_url, caplog):
    caplog.set_level(logging.DEBUG)

    send_jobs(client_with_one_consumer, process_url, jobs=[job])
    wait_until_ready(caplog, [job])


# ------------------------------------------------------------------------
def test_send_multiple_jobs_with_one_consumer(client_with_one_consumer, process_url, jobs, caplog):
    """In this scenario the jobs are processed sequentially."""
    caplog.set_level(logging.DEBUG)

    send_jobs(client_with_one_consumer, process_url, jobs)
    wait_until_ready(caplog, jobs)


# ------------------------------------------------------------------------
def test_send_multiple_jobs_with_three_consumers(client_with_three_consumers, process_url, jobs, caplog):
    """In this scenario the jobs are processed concurrently."""
    caplog.set_level(logging.DEBUG)

    send_jobs(client_with_three_consumers, process_url, jobs)
    wait_until_ready(caplog, jobs)
