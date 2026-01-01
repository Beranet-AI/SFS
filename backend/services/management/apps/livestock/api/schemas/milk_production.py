from pydantic import BaseModel

class MilkProductionSchema(BaseModel):
    volume: float
    ec: float
