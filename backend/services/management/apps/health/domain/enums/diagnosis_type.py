from enum import Enum

class DiagnosisType(str, Enum):
    ROUTINE_CHECK = "routine_check"
    INFECTION = "infection"
    INJURY = "injury"
    CHRONIC = "chronic"
    OTHER = "other"
