from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class RequestValidationOutput:
    valid: bool
    details: Dict[str, Any] | None = None
