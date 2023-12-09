import logging
from time import sleep
from typing import List, Set

from _pytest.logging import LogCaptureFixture

from fastapi_rabbitmq.logger import logger
from fastapi_rabbitmq.messages import Task


# ------------------------------------------------------------------------
def send_tasks(client, process_url:str, tasks: List[Task]) -> None:
    """"""
    for task_ in tasks:
        client.post(process_url, data=task_.model_dump_json())


# ------------------------------------------------------------------------
def wait_until_ready(caplog: LogCaptureFixture, tasks: List[Task]) -> None:
    """"""
    match = {f"Task with correlation_id: {task_.correlation_id} done!!!" for task_ in tasks}
    while not set(caplog.messages).issuperset(match):
        logger.debug("waiting...")
        sleep(1)


# ------------------------------------------------------------------------
def test_send_single_task(client_with_one_consumer, task, process_url, caplog):
    caplog.set_level(logging.DEBUG)

    send_tasks(client_with_one_consumer, process_url, [task])
    wait_until_ready(caplog, [task])


# ------------------------------------------------------------------------
def test_send_multiple_tasks_with_one_consumer(client_with_one_consumer, process_url, tasks, caplog):
    """In this scenario the tasks are processed sequentially."""
    caplog.set_level(logging.DEBUG)

    send_tasks(client_with_one_consumer, process_url, tasks)
    wait_until_ready(caplog, tasks)


# ------------------------------------------------------------------------
def test_send_multiple_tasks_with_three_consumers(client_with_three_consumers, process_url, tasks, caplog):
    """In this scenario the tasks are processed concurrently."""
    caplog.set_level(logging.DEBUG)

    send_tasks(client_with_three_consumers, process_url, tasks)
    wait_until_ready(caplog, tasks)
