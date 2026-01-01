from pydantic import BaseModel

class AIInsightSchema(BaseModel):
    risk_level: str
