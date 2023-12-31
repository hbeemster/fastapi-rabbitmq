import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi_rabbitmq.config import config
from fastapi_rabbitmq.constants import RABBITMQ_URL, QUEUE_NAME
from fastapi_rabbitmq.consumer import JobConsumerContextManager
from fastapi_rabbitmq.messages import Job, Response
from fastapi_rabbitmq.producer import send


# ------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()

    # start as many JobConsumers as needed
    async with JobConsumerContextManager(
        number_of_consumers=config.number_of_consumers,
        loop=loop,
        rabbitmq_url=RABBITMQ_URL,
        queue_name=QUEUE_NAME,
    ) as _:
        yield


# ------------------------------------------------------------------------
# The app
# ------------------------------------------------------------------------
app = FastAPI(lifespan=lifespan)


# ------------------------------------------------------------------------
#  API
# ------------------------------------------------------------------------
@app.post("/process")
async def process(job: Job):
    """"""
    await send(job)
    return Response(success=True, message=f"Started {job.name}")


# ------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------
def main():
    """Start app."""
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
