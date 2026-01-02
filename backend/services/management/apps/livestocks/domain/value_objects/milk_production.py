# File: livestock/domain/value_objects/milk_production.py
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class MilkProduction:
    volume_l: float
    ec: float
    milk_temp_c: Optional[float] = None
    scc: Optional[int] = None
