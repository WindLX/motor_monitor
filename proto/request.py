from pydantic import BaseModel


class CommandRequest(BaseModel):
    command: int
    data: list[dict] | None = None
