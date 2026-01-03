from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class RequestValidationInput:
    payload: Dict[str, Any]
