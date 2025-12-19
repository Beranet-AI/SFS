from apps.health.domain.value_objects.health_status import HealthStatus

class UpdateHealthStatusService:
    """
    Writes current health status into livestock aggregate (delegated).
    """

    def __init__(self, livestock_repo):
        self.livestock_repo = livestock_repo

    def execute(self, livestock_id, status: HealthStatus):
        livestock = self.livestock_repo.get_by_id(livestock_id)
        livestock.update_health(status)
        self.livestock_repo.save(livestock)
        return livestock
