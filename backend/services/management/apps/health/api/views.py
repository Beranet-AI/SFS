from rest_framework.views import APIView
from rest_framework.response import Response
from apps.health.infrastructure.repositories.medical_record_repo_impl import DjangoMedicalRecordRepository
from apps.health.application.services.record_diagnosis import RecordDiagnosisService

class MedicalRecordsView(APIView):
    repo = DjangoMedicalRecordRepository()

    def get(self, request, livestock_id: str):
        records = self.repo.list_by_livestock(livestock_id)
        return Response(records)

    def post(self, request, livestock_id: str):
        svc = RecordDiagnosisService(self.repo)
        record = svc.execute(
            livestock_id=livestock_id,
            diagnosis=request.data["diagnosis"],
            notes=request.data.get("notes", ""),
        )
        return Response({
            "id": record.id,
            "livestock_id": record.livestock_id,
            "diagnosis": record.diagnosis.value,
            "notes": record.notes,
            "recorded_at": record.recorded_at,
        })
