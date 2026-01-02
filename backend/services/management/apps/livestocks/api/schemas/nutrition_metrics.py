from pydantic import BaseModel

class NutritionMetricsSchema(BaseModel):
    feed_intake: float
    water_intake: float
