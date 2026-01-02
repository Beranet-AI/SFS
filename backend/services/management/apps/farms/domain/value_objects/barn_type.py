from enum import Enum


class BarnType(str, Enum):
    FREE_STALL = "free_stall"
    TIE_STALL = "tie_stall"
    OPEN_SHED = "open_shed"
    CLOSED_SHED = "closed_shed"

    @classmethod
    def choices(cls):
        return [(item.value, item.name.replace("_", " ").title()) for item in cls]
