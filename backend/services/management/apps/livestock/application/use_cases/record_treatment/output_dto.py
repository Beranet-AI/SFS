# File: livestock/application/use_cases/record_treatment/output_dto.py
from dataclasses import dataclass
from typing import List

@dataclass
class RecordTreatmentOutputDTO:
    livestock_id: str
    events: List[str]
