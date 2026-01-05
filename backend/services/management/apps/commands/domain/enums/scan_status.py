from enum import Enum


class ScanStatus(str, Enum):
    NEW = "new"
    KNOWN = "known"
    CHANGED = "changed"
