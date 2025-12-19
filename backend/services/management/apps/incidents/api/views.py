from rest_framework.views import APIView
from rest_framework.response import Response
from apps.incidents.infrastructure.models.incident_model import IncidentModel
from apps.incidents.infrastructure.repositories.incident_repo_impl import DjangoIncidentRepository
from apps.incidents.application.use_cases.acknowledge_incident import AcknowledgeIncidentUseCase
from apps.incidents.application.use_cases.resolve_incident import ResolveIncidentUseCase

class IncidentsView(APIView):
    def get(self, request):
        qs = IncidentModel.objects.all().values(
            "id","livestock_id","severity","status","source",
            "description","created_at","acknowledged_at","resolved_at"
        )
        return Response(list(qs))

class IncidentAcknowledgeView(APIView):
    repo = DjangoIncidentRepository()

    def post(self, request, incident_id: str):
        uc = AcknowledgeIncidentUseCase(self.repo)
        incident = uc.execute(incident_id)
        return Response({"id": incident.id, "status": incident.status.value})

class IncidentResolveView(APIView):
    repo = DjangoIncidentRepository()

    def post(self, request, incident_id: str):
        uc = ResolveIncidentUseCase(self.repo)
        incident = uc.execute(incident_id)
        return Response({"id": incident.id, "status": incident.status.value})
