# File: farm/domain/entities/barn.py
from typing import List
from .zone import Zone

class Barn:
    def __init__(self, barn_id: str, name: str):
        self.id = barn_id
        self.name = name
        self.zones: List[Zone] = []

    def add_zone(self, zone: Zone):
        self.zones.append(zone)
