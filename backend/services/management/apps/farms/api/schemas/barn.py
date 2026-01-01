from pydantic import BaseModel

class BarnSchema(BaseModel):
    id: str
    name: str
