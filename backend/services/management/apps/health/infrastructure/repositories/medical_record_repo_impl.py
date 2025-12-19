from apps.health.domain.entities.medical_record import MedicalRecord
from apps.health.infrastructure.models.medical_record_model import MedicalRecordModel
from shared.ids.livestock_id import LivestockId
from apps.health.domain.enums.diagnosis_type import DiagnosisType

class DjangoMedicalRecordRepository:

    def add(self, record: MedicalRecord) -> MedicalRecord:
        obj = MedicalRecordModel.objects.create(
            livestock_id=str(record.livestock_id),
            diagnosis=record.diagnosis.value,
            notes=record.notes,
            recorded_at=record.recorded_at,
        )
        return MedicalRecord(
            id=str(obj.id),
            livestock_id=LivestockId(obj.livestock_id),
            diagnosis=DiagnosisType(obj.diagnosis),
            notes=obj.notes,
            recorded_at=obj.recorded_at,
        )

    def list_by_livestock(self, livestock_id: LivestockId):
        qs = MedicalRecordModel.objects.filter(livestock_id=str(livestock_id))
        return list(qs.values())
