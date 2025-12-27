from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.telemetry.application.services.telemetry_service import TelemetryService
from apps.telemetry.api.serializers import TelemetryIngestSerializer, TelemetrySerializer


class TelemetryIngestView(APIView):
    service = TelemetryService()

    def post(self, request):
        ser = TelemetryIngestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        obj = self.service.ingest(**ser.validated_data)

        return Response(
            TelemetrySerializer(obj).data,
            status=status.HTTP_201_CREATED,
        )


class TelemetryRecentView(APIView):
    service = TelemetryService()

    def get(self, request, livestock_id: str):
        limit = int(request.query_params.get("limit", 100))
        qs = self.service.list_recent(livestock_id=livestock_id, limit=limit)

        return Response(
            TelemetrySerializer(qs, many=True).data,
            status=status.HTTP_200_OK,
        )
