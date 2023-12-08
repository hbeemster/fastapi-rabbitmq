import json
from random import randrange

from fastapi_rabbitmq.producer import send
import requests

def test_send_task():
    data = {"name": "TADA", "duration": 0.3}
    response = requests.post('http://127.0.0.1:8000/process', data=json.dumps(data))

    assert response


def test_send_multiple_tasks():
    for index in range(10):
        duration = randrange(1, 50) / 10
        data = {"name": f"Task-{index}", "duration": duration}
        _ = requests.post('http://127.0.0.1:8000/process', data=json.dumps(data))


