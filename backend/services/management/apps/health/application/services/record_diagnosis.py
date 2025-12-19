from datetime import datetime
from apps.health.domain.entities.medical_record import MedicalRecord

class RecordDiagnosisService:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, livestock_id, diagnosis, notes: str):
        record = MedicalRecord(
            id="",
            livestock_id=livestock_id,
            diagnosis=diagnosis,
            notes=notes,
            recorded_at=datetime.utcnow(),
        )
        return self.repo.add(record)
