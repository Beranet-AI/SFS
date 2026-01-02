# File: livestock/application/use_cases/record_treatment/use_case.py
from ....domain.value_objects.disease_record import DiseaseRecord

class RecordTreatmentUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, input_dto):
        livestock = self.repo.get_by_id(input_dto.livestock_id)

        if input_dto.disease_name and input_dto.diagnosed_at:
            livestock.diagnose_disease(DiseaseRecord(
                disease_name=input_dto.disease_name,
                diagnosed_at=input_dto.diagnosed_at,
                medication_name=input_dto.medication_name,
                milk_withdrawal_days=input_dto.milk_withdrawal_days,
            ))

        if input_dto.treatment_completed and input_dto.medication_name:
            livestock.complete_treatment(input_dto.medication_name)

        self.repo.save(livestock)
        events = [e.__class__.__name__ for e in livestock.pull_events()]
        return {"livestock_id": livestock.id, "events": events}
