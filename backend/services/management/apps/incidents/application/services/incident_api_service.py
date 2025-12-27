from apps.incidents.models import IncidentModel


class IncidentApiService:
    """
    Application-layer orchestration for Incidents API.
    All ORM access lives here.
    """

    def list_incidents(self):
        return IncidentModel.objects.all().order_by("-ts")

    def create_incident(self, *, validated_data: dict):
        return IncidentModel.objects.create(**validated_data)
