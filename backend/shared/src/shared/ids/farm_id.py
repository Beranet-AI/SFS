from dataclasses import dataclass

@dataclass(frozen=True)
class FarmId:
    value: str
    def __str__(self) -> str:
        return self.value
