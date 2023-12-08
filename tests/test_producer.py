import logging
from time import sleep

from fastapi_rabbitmq.logger import logger
from fastapi_rabbitmq.messages import Task


def test_send_task(client, caplog):
    caplog.set_level(logging.DEBUG)

    data = {"name": "TADA", "duration": 3.0}
    task = Task(**data)
    response = client.post("http://127.0.0.1:8000/process", data=task.model_dump_json())

    assert response

    while f"Task with correlation_id: {task.correlation_id} done!!!" not in caplog.text:
        logger.debug("waiting...")
        sleep(1)
    # # while response := client.get('http://127.0.0.1:8000/task_count'):
    # #
    # #     print("Wait for task in queue")
    # #     if response.json()["count"] > 0:
    # #         break
    # #     sleep(0.01)
    #
    #
    # while response := client.get('http://127.0.0.1:8000/task_count'):
    #     sleep(0.01)
    #     print("Wait for empty queue")
    #     if response.json()["count"] == 0:
    #         break


# def test_send_multiple_tasks():
#     for index in range(10):
#         duration = randrange(1, 50) / 10
#         data = {"name": f"Task-{index}", "duration": duration}
#         _ = requests.post('http://127.0.0.1:8000/process', data=json.dumps(data))
