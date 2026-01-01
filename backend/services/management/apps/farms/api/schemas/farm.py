from pydantic import BaseModel

class FarmSchema(BaseModel):
    id: str
    name: str
