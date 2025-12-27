from rest_framework.views import APIView
from rest_framework.response import Response

from apps.health.infrastructure.repositories.medical_record_repo_impl import (
    DjangoMedicalRecordRepository,
)
from apps.health.application.services.health_service import HealthService


class MedicalRecordsView(APIView):

    def get(self, request, livestock_id: str):
        service = HealthService(DjangoMedicalRecordRepository())
        records = service.list_by_livestock(livestock_id=livestock_id)

        return Response([
            {
                "id": r.id,
                "livestock_id": r.livestock_id,
                "diagnosis": r.diagnosis.value,
                "notes": r.notes,
                "recorded_at": r.recorded_at,
            }
            for r in records
        ])

    def post(self, request, livestock_id: str):
        service = HealthService(DjangoMedicalRecordRepository())

        record = service.record_diagnosis(
            livestock_id=livestock_id,
            diagnosis=request.data["diagnosis"],
            notes=request.data.get("notes", ""),
        )

        return Response(
            {
                "id": record.id,
                "livestock_id": record.livestock_id,
                "diagnosis": record.diagnosis.value,
                "notes": record.notes,
                "recorded_at": record.recorded_at,
            },
            status=201,
        )
