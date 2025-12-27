from apps.incidents.models import IncidentModel



class IncidentService:
    """
    Application service for incident lifecycle management.
    All ORM access lives here.
    """

    def get_by_id(self, *, incident_id: str) -> IncidentModel:
        incident = IncidentModel.objects.get(id=str(incident_id))
        return IncidentModel(incident)

    def create_incident(
        self,
        *,
        title: str,
        severity: str,
        source: str,
        description: str = "",
        device_id: str | None = None,
        livestock_id: str | None = None,
        source_ref: str | None = None,
    ) -> IncidentModel:
        incident = IncidentModel.objects.create(
            title=title,
            severity=severity,
            source=source,
            description=description,
            device_id=device_id,
            livestock_id=livestock_id,
            source_ref=source_ref,
        )
        return IncidentModel(incident)

    def acknowledge(self, *, incident_id: str) -> IncidentModel:
        incident = IncidentModel.objects.get(id=str(incident_id))
        incident.acknowledge()
        return IncidentModel(incident)

    def resolve(self, *, incident_id: str) -> IncidentModel:
        incident = IncidentModel.objects.get(id=str(incident_id))
        incident.resolve()
        return IncidentModel(incident)
