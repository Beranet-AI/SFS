from abc import ABC, abstractmethod
from apps.livestock.domain.entities.livestock import Livestock

class LivestockRepository(ABC):
    @abstractmethod
    def get_by_id(self, livestock_id: str) -> Livestock: ...
    @abstractmethod
    def save(self, livestock: Livestock) -> None: ...
