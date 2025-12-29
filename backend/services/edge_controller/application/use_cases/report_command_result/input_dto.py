from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ReportCommandResultInputDTO:
    result_payload: Dict[str, Any]
