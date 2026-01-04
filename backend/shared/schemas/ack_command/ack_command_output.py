from dataclasses import dataclass


@dataclass
class AckCommandOutput:
    ok: bool
