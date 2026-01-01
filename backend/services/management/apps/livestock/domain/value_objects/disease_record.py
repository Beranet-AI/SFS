# File: livestock/domain/value_objects/disease_record.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class DiseaseRecord:
    disease_name: str
    diagnosed_at: datetime
    medication_name: Optional[str] = None
    milk_withdrawal_days: Optional[int] = None
