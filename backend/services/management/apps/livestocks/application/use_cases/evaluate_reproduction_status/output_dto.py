# File: livestock/application/use_cases/evaluate_reproduction_status/output_dto.py
from dataclasses import dataclass
from typing import List

@dataclass
class EvaluateReproductionStatusOutputDTO:
    livestock_id: str
    events: List[str]
