# farm/domain/repositories/farm_repository.py
from abc import ABC, abstractmethod
from ..entities.farm import Farm


class FarmRepository(ABC):
    @abstractmethod
    def get_by_id(self, farm_id: str) -> Farm: ...

    @abstractmethod
    def save(self, farm: Farm) -> None: ...
