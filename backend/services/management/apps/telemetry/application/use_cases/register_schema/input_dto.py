# application/use_cases/register_schema/input_dto.py

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class RegisterSchemaInputDTO:
    device_type: str
    json_schema: Dict[str, Any]
    raw_example: Dict[str, Any]
    created_by: str
