from dataclasses import dataclass


@dataclass(frozen=True)
class ScanId:
    value: str
