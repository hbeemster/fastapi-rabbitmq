"""Main logger module."""

import logging
from pathlib import Path

path = Path(__file__).parents[2] / "logs"
path.mkdir(exist_ok=True)
filename = path / "fastapi_rabbitmq.log"


logger = logging.getLogger("fastapi_rabbitmq")
f_handler = logging.FileHandler(filename)
f_handler.setLevel(logging.DEBUG)
f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)
