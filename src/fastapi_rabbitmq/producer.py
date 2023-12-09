import aio_pika

from fastapi_rabbitmq.asyncio_helpers import create_task_for_event_loop
from fastapi_rabbitmq.constants import ROUTING_KEY, RABBITMQ_URL
from fastapi_rabbitmq.messages import Job

# ------------------------------------------------------------------------
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

# ------------------------------------------------------------------------
async def send(job: Job):
    create_task_for_event_loop(main, job)

