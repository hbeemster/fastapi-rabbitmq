"""Module with asyncio helpers."""
import asyncio

from fastapi_rabbitmq.logger import logger


def create_task_for_event_loop(coro, *args, **kwargs):
    """This function will create task for the event loop for asyncio coroutines.

    It wil try to get the running event loop, if there is no running event loop it will create a new one.
    After that it will create a asyncio task for the given coroutine and any arguments passed to the coroutine.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # 'RuntimeError: There is no current event loop...'
        loop = None

    if loop and loop.is_running():
        logger.debug("Async event loop already running.")
    else:
        logger.debug("Create a new event loop")
        loop = asyncio.new_event_loop()
    # Create a Task for the loop
    loop.create_task(coro(*args, **kwargs))
