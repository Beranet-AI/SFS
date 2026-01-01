# File: farm/domain/value_objects/location.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Location:
    country: str
    city: str
    latitude: float
    longitude: float
