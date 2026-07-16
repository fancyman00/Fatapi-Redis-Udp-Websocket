from typing import Union

from pydantic import BaseModel, Json

from app.schemas.telemetry import InfraredMatrix


class Message(BaseModel):
    channel: str
    event: str
    data: Union[InfraredMatrix, None] = None


