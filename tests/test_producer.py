import logging
from time import sleep

from fastapi_rabbitmq.logger import logger
from fastapi_rabbitmq.messages import Task


def test_send_single_task(client_with_one_consumer, caplog):
    caplog.set_level(logging.DEBUG)

    data = {"name": "TADA", "duration": 3.0}
    task = Task(**data)
    response = client_with_one_consumer.post("http://127.0.0.1:8000/process", data=task.model_dump_json())

    assert response

    # sourcery skip: no-loop-in-tests
    while f"Task with correlation_id: {task.correlation_id} done!!!" not in caplog.text:
        logger.debug("waiting...")
        sleep(1)


def test_send_multiple_tasks_with_one_consumer(client_with_one_consumer, tasks, caplog):
    """In this scenario the tasks are processed sequentially."""
    caplog.set_level(logging.DEBUG)

    for task in tasks:
        response = client_with_one_consumer.post("http://127.0.0.1:8000/process", data=task.model_dump_json())
        assert response

    # sourcery skip: no-loop-in-tests
    match = {f"Task with correlation_id: {task_.correlation_id} done!!!" for task_ in tasks}
    while not set(caplog.messages).issuperset(match):
        logger.debug("waiting...")
        sleep(1)

def test_send_multiple_tasks_with_three_consumers(client_with_three_consumers, tasks, caplog):
    """In this scenario the tasks are processed concurrently."""
    caplog.set_level(logging.DEBUG)

    for task in tasks:
        response = client_with_three_consumers.post("http://127.0.0.1:8000/process", data=task.model_dump_json())
        assert response

    # sourcery skip: no-loop-in-tests
    match = {f"Task with correlation_id: {task_.correlation_id} done!!!" for task_ in tasks}
    while not set(caplog.messages).issuperset(match):
        logger.debug("waiting...")
        sleep(1)
