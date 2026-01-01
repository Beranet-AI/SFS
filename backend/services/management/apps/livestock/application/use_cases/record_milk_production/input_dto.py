# File: livestock/application/use_cases/record_milk_production/input_dto.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class RecordMilkProductionInputDTO:
    livestock_id: str
    volume_l: float
    ec: float
    milk_temp_c: Optional[float] = None
    scc: Optional[int] = None
