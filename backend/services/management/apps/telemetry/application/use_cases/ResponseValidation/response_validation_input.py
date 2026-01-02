from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ResponseValidationInput:
    payload: Dict[str, Any]
