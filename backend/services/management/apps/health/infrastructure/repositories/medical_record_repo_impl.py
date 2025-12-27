from apps.health.models import MedicalRecordModel
from apps.health.domain.entities.medical_record import MedicalRecord
from apps.health.domain.repositories.medical_record_repo import MedicalRecordRepository


class DjangoMedicalRecordRepository(MedicalRecordRepository):

    def list_by_livestock(self, livestock_id: str):
        return [
            MedicalRecord.from_orm(obj)
            for obj in MedicalRecordModel.objects
            .filter(livestock_id=livestock_id)
            .order_by("-recorded_at")
        ]

    def save(self, record: MedicalRecord) -> MedicalRecord:
        obj = MedicalRecordModel.objects.create(
            livestock_id=record.livestock_id,
            diagnosis=record.diagnosis.value,
            notes=record.notes,
            recorded_at=record.recorded_at,
        )
        return MedicalRecord.from_orm(obj)
