# File: livestock/application/use_cases/register_livestock/output_dto.py
from dataclasses import dataclass

@dataclass
class RegisterLivestockOutputDTO:
    livestock_id: str
