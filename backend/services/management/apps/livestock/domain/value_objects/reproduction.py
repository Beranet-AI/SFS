# File: livestock/domain/value_objects/reproduction.py
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass(frozen=True)
class ReproductionStatus:
    estrus: bool
    pregnant: bool
    insemination_date: Optional[date] = None
    insemination_method: Optional[str] = None  # "NATURAL" | "AI"
    insemination_result: Optional[str] = None  # "PENDING" | "SUCCESS" | "FAILED"
    calving_date: Optional[date] = None
