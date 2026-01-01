# File: livestock/application/use_cases/record_health_metrics/output_dto.py
from dataclasses import dataclass
from typing import List

@dataclass
class RecordHealthMetricsOutputDTO:
    livestock_id: str
    events: List[str]
