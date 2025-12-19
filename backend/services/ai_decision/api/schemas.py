from pydantic import BaseModel

class DecisionRequest(BaseModel):
    livestock_id: str
