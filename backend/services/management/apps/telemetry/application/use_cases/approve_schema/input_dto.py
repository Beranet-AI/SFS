# application/use_cases/approve_schema/input_dto.py

from dataclasses import dataclass


@dataclass
class ApproveSchemaInputDTO:
    schema_id: str
    approved_by: str
