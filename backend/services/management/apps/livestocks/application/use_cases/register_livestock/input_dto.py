# File: livestock/application/use_cases/register_livestock/input_dto.py
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class RegisterLivestockInputDTO:
    livestock_id: str
    tag_id: str
    breed: str
    birth_date: Optional[date]
    sex: str
    herd_entry_date: Optional[date]
    status: str
