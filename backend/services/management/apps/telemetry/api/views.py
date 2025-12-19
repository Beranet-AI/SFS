from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.telemetry.infrastructure.repositories.telemetry_repo_impl import DjangoTelemetryRepository
from apps.telemetry.application.services.ingest_telemetry import IngestTelemetryService

class TelemetryIngestView(APIView):
    repo = DjangoTelemetryRepository()

    def post(self, request):
        svc = IngestTelemetryService(self.repo)
        record = svc.ingest(
            device_id=request.data["device_id"],
            livestock_id=request.data["livestock_id"],
            metric=request.data["metric"],
            value=float(request.data["value"]),
        )
        return Response(
            {
                "device_id": record.device_id,
                "livestock_id": record.livestock_id,
                "metric": record.metric,
                "value": record.value,
                "recorded_at": record.recorded_at,
            },
            status=status.HTTP_201_CREATED,
        )

class TelemetryRecentView(APIView):
    repo = DjangoTelemetryRepository()

    def get(self, request, livestock_id: str):
        data = self.repo.list_recent(livestock_id)
        return Response(data)
