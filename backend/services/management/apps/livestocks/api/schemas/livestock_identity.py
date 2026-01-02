from pydantic import BaseModel

class LivestockIdentitySchema(BaseModel):
    tag_id: str
    breed: str
