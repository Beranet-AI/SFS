from pydantic import BaseModel

class ReproductionSchema(BaseModel):
    estrus: bool
    pregnant: bool
