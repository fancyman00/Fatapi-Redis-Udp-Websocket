from pydantic import BaseModel


class InfraredMatrix(BaseModel):
    data: list[float]
