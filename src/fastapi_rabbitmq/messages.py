import uuid
from typing import Any

from pydantic import BaseModel


# ------------------------------------------------------------------------
class Response(BaseModel):
    success: bool
    message: str = ""


# ------------------------------------------------------------------------
class ResponseTaskCount(BaseModel):
    success: bool
    count: int


# ------------------------------------------------------------------------
class Task(BaseModel):
    name: str
    duration: float | None = 0.1
    correlation_id: str | None = None

    def model_post_init(self, __context: Any) -> None:
        if not self.correlation_id:
            self.correlation_id = str(uuid.uuid4())
