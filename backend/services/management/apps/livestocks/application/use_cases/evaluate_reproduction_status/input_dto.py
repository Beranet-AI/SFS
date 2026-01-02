# File: livestock/application/use_cases/evaluate_reproduction_status/input_dto.py
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class EvaluateReproductionStatusInputDTO:
    livestock_id: str
    estrus: bool
    pregnant: bool
    insemination_date: Optional[date] = None
    insemination_method: Optional[str] = None
    insemination_result: Optional[str] = None
    calving_date: Optional[date] = None
