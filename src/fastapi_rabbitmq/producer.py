import asyncio

import aio_pika

from fastapi_rabbitmq.constants import ROUTING_KEY, RABBITMQ_URL
from fastapi_rabbitmq.logger import logger
from fastapi_rabbitmq.messages import Job


async def main(task: Job) -> None:
    connection = await aio_pika.connect_robust(
        RABBITMQ_URL,
    )

    async with connection:
        routing_key = ROUTING_KEY

        channel = await connection.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(body=task.model_dump_json().encode("utf-8")),
            routing_key=routing_key,
        )


def send(task: Job):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # 'RuntimeError: There is no current event loop...'
        loop = None

    if loop and loop.is_running():
        logger.debug("Async event loop already running. Adding coroutine to the event loop.")
        tsk = loop.create_task(main(task))
        # Optionally, a callback function can be executed when the coroutine completes
        tsk.add_done_callback(lambda t: logger.debug(f"Task done with result={t.result()}  << return val of main()"))
    else:
        logger.debug("Starting new event loop")
        asyncio.run(main(task))

