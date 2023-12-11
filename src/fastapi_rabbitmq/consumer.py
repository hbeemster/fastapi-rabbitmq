# from controllers import new_log
import asyncio
import json
from asyncio import sleep

import aio_pika

from fastapi_rabbitmq.logger import logger
from fastapi_rabbitmq.messages import Job


# ------------------------------------------------------------------------
# JobConsumer
# ------------------------------------------------------------------------
class JobConsumer:
    """The TaskConsumer class takes care of processing the Tasks."""

    # ------------------------------------------------------------------------
    def __init__(
        self,
        *,
        loop: asyncio.AbstractEventLoop,
        rabbitmq_url: str,
        queue_name: str,
    ) -> None:
        self.loop = loop
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.connection = None

    # ------------------------------------------------------------------------
    async def process_message(self, message: aio_pika.IncomingMessage):
        message_ = json.loads(message.body.decode("utf-8"))
        job = Job(**message_)

        logger.info(75 * "=")
        logger.info(message_)
        logger.info("start crunching...")
        await sleep(job.duration)
        logger.info(f"Job with correlation_id: {job.correlation_id} done!!!")
        logger.info(75 * "=")
        await message.ack()

    # ------------------------------------------------------------------------
    async def start_consumer(self) -> None:
        logger.debug(f"Start consumer: {self}")
        self.connection = await aio_pika.connect(self.rabbitmq_url, loop=self.loop)
        channel = await self.connection.channel()
        await channel.set_qos(prefetch_count=1)
        queue = await channel.declare_queue(self.queue_name)
        await queue.consume(self.process_message)

    # ------------------------------------------------------------------------
    async def stop_consumer(self) -> None:
        await self.connection.close()


# ------------------------------------------------------------------------
# JobConsumerContextManager
# ------------------------------------------------------------------------
class JobConsumerContextManager:
    """This context manager lets you create one or more TaskConsumers.

    Cleanup is done when the context manager exits.
    """

    # ------------------------------------------------------------------------
    def __init__(
        self,
        *,
        number_of_consumers: int,
        loop: asyncio.AbstractEventLoop,
        rabbitmq_url: str,
        queue_name: str,
    ):
        self.number_of_consumers = number_of_consumers
        self.loop = loop
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.consumers = []

    # ------------------------------------------------------------------------
    async def __aenter__(self):
        for _ in range(self.number_of_consumers):
            consumer = JobConsumer(loop=self.loop, rabbitmq_url=self.rabbitmq_url, queue_name=self.queue_name)
            self.consumers.append(consumer)
            await consumer.start_consumer()
        return self

    # ------------------------------------------------------------------------
    async def __aexit__(self, exc_type, exc, tb):
        for consumer in self.consumers:
            await consumer.stop_consumer()
