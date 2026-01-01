# farm/application/use_cases/register_barn/input_dto.py
from dataclasses import dataclass

@dataclass
class RegisterBarnInputDTO:
    farm_id: str
    barn_id: str
    name: str
