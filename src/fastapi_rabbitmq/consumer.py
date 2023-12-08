# from controllers import new_log
import json
from asyncio import sleep

import aio_pika
from aio_pika.abc import AbstractChannel

from fastapi_rabbitmq.constants import QUEUE_NAME
from fastapi_rabbitmq.logger import logger
from fastapi_rabbitmq.messages import Task


async def init_queue(channel: AbstractChannel):
    queue = await channel.declare_queue(QUEUE_NAME)
    await queue.consume(on_message)
    return QUEUE_NAME, queue


async def on_message(message: aio_pika.IncomingMessage):
    # tracker = ast.literal_eval(message.body.decode("utf-8"))
    message_ = json.loads(message.body.decode("utf-8"))

    task = Task(**message_)
    logger.info(75 * "=")
    logger.info(message_)
    logger.info("start crunching...")
    await sleep(task.duration)
    logger.info(f"Task with correlation_id: {task.correlation_id} done!!!")
    logger.info(75 * "=")
    await message.ack()

    #
    # new_log(tracker["ip_address"], tracker["request_url"], tracker["request_port"],
    #                     tracker["request_path"], tracker["request_method"],
    #                     tracker["browser_type"],tracker["request_time"], tracker["service_name"])
