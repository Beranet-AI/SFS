from pydantic import BaseModel


class ReceiveTelemetryResponse(BaseModel):
    status: str
