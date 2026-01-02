# File: livestock/domain/domain_events/treatment_completed.py
class TreatmentCompleted:
    def __init__(self, livestock_id: str, medication_name: str):
        self.livestock_id = livestock_id
        self.medication_name = medication_name
