from dataclasses import dataclass
from shared.value_objects.livestock_location import LivestockLocation
from apps.livestock.domain.value_objects.health_status import HealthStatus

@dataclass
class Livestock:
    id: str
    tag: str
    location: LivestockLocation
    health_status: HealthStatus

    def update_health(self, new_status: HealthStatus) -> None:
        self.health_status = new_status
