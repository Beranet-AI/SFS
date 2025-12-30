# application/use_cases/register_schema/output_dto.py

from dataclasses import dataclass


@dataclass
class RegisterSchemaOutputDTO:
    schema_id: str
    version: str
