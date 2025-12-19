from abc import ABC, abstractmethod
from apps.farms.domain.entities.farm import Farm

class FarmRepository(ABC):
    @abstractmethod
    def get_by_id(self, farm_id: str) -> Farm: ...
    @abstractmethod
    def create(self, farm: Farm) -> Farm: ...
