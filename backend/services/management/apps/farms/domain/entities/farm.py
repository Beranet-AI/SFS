# farm/domain/entities/farm.py
from typing import List, Optional
from .barn import Barn
from ..value_objects.location import Location
from ..value_objects.economic_metrics import EconomicMetrics
from ..domain_events.farm_created import FarmCreated
from ..domain_events.barn_added import BarnAdded
from ..domain_events.zone_added import ZoneAdded

class Farm:
    """
    Aggregate Root
    """
    def __init__(self, farm_id: str, name: str, location: Location):
        self.id = farm_id
        self.name = name
        self.location = location
        self.barns: List[Barn] = []
        self.economic: Optional[EconomicMetrics] = None
        self._events: List[object] = []

    @staticmethod
    def create(farm_id: str, name: str, location: Location):
        farm = Farm(farm_id, name, location)
        farm._events.append(FarmCreated(farm_id))
        return farm

    def add_barn(self, barn: Barn):
        self.barns.append(barn)
        self._events.append(BarnAdded(self.id, barn.id))

    def add_zone(self, barn_id: str, zone):
        barn = next(b for b in self.barns if b.id == barn_id)
        barn.add_zone(zone)
        self._events.append(ZoneAdded(self.id, barn_id, zone.id))

    def set_economic_metrics(self, econ: EconomicMetrics):
        self.economic = econ

    def pull_events(self):
        ev = self._events[:]
        self._events.clear()
        return ev
