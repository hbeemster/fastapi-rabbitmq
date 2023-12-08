from pydantic import BaseModel


# ------------------------------------------------------------------------
class Response(BaseModel):
    success: bool
    message: str = ""


# ------------------------------------------------------------------------
class Task(BaseModel):
    name: str
    duration: float | None = 0.1
