from datetime import datetime
from apps.health.domain.repositories.medical_record_repo import MedicalRecordRepository
from apps.health.domain.entities.medical_record import MedicalRecord


class HealthService:
    """
    Application service for health / medical records.
    """

    def __init__(self, repo: MedicalRecordRepository):
        self.repo = repo

    # -------------------------
    # Queries
    # -------------------------

    def list_by_livestock(self, *, livestock_id: str):
        return self.repo.list_by_livestock(livestock_id)

    # -------------------------
    # Commands
    # -------------------------

    def record_diagnosis(
        self,
        *,
        livestock_id: str,
        diagnosis: str,
        notes: str = "",
        recorded_at: datetime | None = None,
    ) -> MedicalRecord:
        record = MedicalRecord.create(
            livestock_id=livestock_id,
            diagnosis=diagnosis,
            notes=notes,
            recorded_at=recorded_at or datetime.utcnow(),
        )
        return self.repo.save(record)
