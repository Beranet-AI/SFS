# farm/application/use_cases/register_farm/input_dto.py
from dataclasses import dataclass

@dataclass
class RegisterFarmInputDTO:
    farm_id: str
    name: str
    country: str
    city: str
    latitude: float
    longitude: float
