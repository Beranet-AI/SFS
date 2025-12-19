from shared.ids.farm_id import FarmId
from shared.value_objects.livestock_location import LivestockLocation
from shared.enums.health_state import HealthState

from apps.livestock.domain.entities.livestock import Livestock
from apps.livestock.domain.value_objects.health_status import HealthStatus
from apps.livestock.infrastructure.models.livestock_model import LivestockModel

class DjangoLivestockRepository:
    def get_by_id(self, livestock_id: str) -> Livestock:
        obj = LivestockModel.objects.get(id=livestock_id)
        return Livestock(
            id=str(obj.id),
            tag=obj.tag,
            location=LivestockLocation(farm_id=FarmId(obj.farm_id), barn=obj.barn, zone=obj.zone),
            health_status=HealthStatus(
                state=HealthState(obj.health_state),
                confidence=obj.health_confidence,
                evaluated_at=obj.health_evaluated_at,
            ),
        )

    def save(self, livestock: Livestock) -> None:
        LivestockModel.objects.update_or_create(
            id=livestock.id,
            defaults={
                "tag": livestock.tag,
                "farm_id": str(livestock.location.farm_id),
                "barn": livestock.location.barn,
                "zone": livestock.location.zone,
                "health_state": livestock.health_status.state.value,
                "health_confidence": livestock.health_status.confidence,
                "health_evaluated_at": livestock.health_status.evaluated_at,
            },
        )
