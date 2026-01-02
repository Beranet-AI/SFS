
from dataclasses import dataclass

@dataclass
class DetectHealthAnomalyOutputDTO:
    ever: bool
    severe: bool

