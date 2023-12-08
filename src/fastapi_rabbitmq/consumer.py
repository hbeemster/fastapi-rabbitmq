
# from controllers import new_log
import json
from asyncio import sleep

import aio_pika
import ast

from fastapi_rabbitmq.messages import Task


async def on_message(message: aio_pika.IncomingMessage):
    # tracker = ast.literal_eval(message.body.decode("utf-8"))
    message_ = json.loads(message.body.decode("utf-8"))

    task = Task(**message_)
    print(75 * "=")
    print(message_)
    print("start crunching...")
    # await sleep(task.duration)
    print("done!!!")
    print(75 * "=")
    await message.ack()

    #
    # new_log(tracker["ip_address"], tracker["request_url"], tracker["request_port"],
    #                     tracker["request_path"], tracker["request_method"],
    #                     tracker["browser_type"],tracker["request_time"], tracker["service_name"])


