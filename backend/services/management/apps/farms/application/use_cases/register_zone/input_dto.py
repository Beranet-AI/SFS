# farm/application/use_cases/register_zone/input_dto.py
from dataclasses import dataclass

@dataclass
class RegisterZoneInputDTO:
    farm_id: str
    barn_id: str
    zone_id: str
    name: str
