# File: livestock/application/use_cases/record_milk_production/output_dto.py
from dataclasses import dataclass

@dataclass
class RecordMilkProductionOutputDTO:
    livestock_id: str
