# application/use_cases/approve_schema/output_dto.py

from dataclasses import dataclass


@dataclass
class ApproveSchemaOutputDTO:
    success: bool
    activated_version: str
