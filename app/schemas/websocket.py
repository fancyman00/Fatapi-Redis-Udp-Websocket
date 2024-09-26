from typing import Union

from pydantic import BaseModel, Json

from app.schemas.telemetry import InfraredMatrix


class WebsocketMessage(BaseModel):
    event: list[str]
    message: Json[Union[InfraredMatrix, None]] = None


