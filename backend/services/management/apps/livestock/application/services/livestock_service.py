from django.utils import timezone

from apps.livestock.models import LivestockModel
from apps.livestock.domain.rules.health_rules import HealthRules


class LivestockService:
    """
    Application service for Livestock lifecycle and health management.
    """

    # ---------- Queries ----------

    def get_by_id(self, *, livestock_id: str) -> LivestockModel:
        return LivestockModel.objects.get(id=livestock_id)

    def list_all(self):
        return LivestockModel.objects.all()

    def list_by_farm(self, *, farm_id: str):
        return LivestockModel.objects.filter(farm_id=farm_id)

    # ---------- Commands ----------

    def update_health_from_score(
        self,
        *,
        livestock_id: str,
        score: float,
    ) -> LivestockModel:

        livestock = self.get_by_id(livestock_id=livestock_id)

        health_status = HealthRules.from_score(score)

        livestock.health_state = health_status.state.value
        livestock.health_confidence = health_status.confidence
        livestock.health_evaluated_at = (
            health_status.evaluated_at or timezone.now()
        )

        livestock.save(
            update_fields=[
                "health_state",
                "health_confidence",
                "health_evaluated_at",
            ]
        )

        return livestock
