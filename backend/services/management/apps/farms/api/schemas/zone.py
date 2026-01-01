from pydantic import BaseModel

class ZoneSchema(BaseModel):
    id: str
    name: str
