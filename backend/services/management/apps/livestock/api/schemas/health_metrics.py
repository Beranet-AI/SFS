from pydantic import BaseModel

class HealthMetricsSchema(BaseModel):
    temperature: float
    activity: float
