from pydantic import BaseModel


class MotorMessageRequest(BaseModel):
    command: int
    data: list[dict] | None = None
