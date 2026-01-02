# File: livestock/application/use_cases/record_treatment/input_dto.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class RecordTreatmentInputDTO:
    livestock_id: str
    disease_name: Optional[str]
    diagnosed_at: Optional[datetime]
    medication_name: Optional[str]
    milk_withdrawal_days: Optional[int]
    treatment_completed: bool = False
