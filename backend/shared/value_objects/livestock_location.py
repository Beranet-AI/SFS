from dataclasses import dataclass
from shared.ids.farm_id import FarmId

@dataclass(frozen=True)
class LivestockLocation:
    """
    Represents the physical location of a livestock.
    Composed of farm + barn + zone.
    """
    farm_id: FarmId
    barn: str
    zone: str

    def __post_init__(self):
        if not self.barn:
            raise ValueError("Barn cannot be empty")
        if not self.zone:
            raise ValueError("Zone cannot be empty")
