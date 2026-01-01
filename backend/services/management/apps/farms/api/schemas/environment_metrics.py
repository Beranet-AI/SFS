from pydantic import BaseModel

class EnvironmentMetricsSchema(BaseModel):
    temperature: float
    humidity: float
    ammonia: float
