import asyncio
from contextlib import asynccontextmanager

import aio_pika
from fastapi import FastAPI

from fastapi_rabbitmq.constants import RABBITMQ_URL, QUEUE_NAME
from fastapi_rabbitmq.consumer import init_queue
from fastapi_rabbitmq.messages import Task, Response, ResponseTaskCount
from fastapi_rabbitmq.producer import send


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    connection = await aio_pika.connect(RABBITMQ_URL, loop=loop)
    channel = await connection.channel()
    queue_name, queue = await init_queue(channel)
    app.queues = {queue_name: queue}

    yield

    await connection.close()


app = FastAPI(lifespan=lifespan)


# ------------------------------------------------------------------------
@app.post("/process")
async def process(task: Task):
    send(task)
    return Response(success=True, message=f"Started {task.name}")


# ------------------------------------------------------------------------
@app.get("/task_count")
async def task_count():
    queue = app.queues[QUEUE_NAME]
    return ResponseTaskCount(success=True, count=queue.declaration_result.message_count)


# ------------------------------------------------------------------------
@app.get("/")
async def hello():
    return "hello"


# ------------------------------------------------------------------------
def main():
    """Start app."""
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
