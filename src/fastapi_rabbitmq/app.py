from contextlib import asynccontextmanager

from fastapi import FastAPI


import asyncio
import aio_pika

from fastapi_rabbitmq.constants import RABBITMQ_URL, QUEUE_NAME
from fastapi_rabbitmq.consumer import on_message
from fastapi_rabbitmq.messages import Task, Response
from fastapi_rabbitmq.producer import send

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    loop = asyncio.get_event_loop()
    connection = await aio_pika.connect(RABBITMQ_URL, loop=loop)
    channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME)
    await queue.consume(on_message)

    yield

    await connection.close()


app = FastAPI(lifespan=lifespan)


# @app.on_event("startup")
# async def startup():
#     loop = asyncio.get_event_loop()
#     connection = await aio_pika.connect(RABBITMQ_URL, loop=loop)
#     channel = await connection.channel()
#     queue = await channel.declare_queue("test_process")
#     await queue.consume(on_message)


@app.post("/process")
async def process(task: Task):
    send(task)
    return Response(success=True, message=f"Started {task.name}")



@app.get("/")
async def hello():
    return "hello"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

