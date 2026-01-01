from pydantic import BaseModel
from typing import Optional

class DiseaseSchema(BaseModel):
    disease_name: Optional[str] = None
    diagnosed_at: Optional[str] = None
    treatment_name: Optional[str] = None
