# File: livestock/domain/domain_events/disease_diagnosed.py
class DiseaseDiagnosed:
    def __init__(self, livestock_id: str, disease_name: str):
        self.livestock_id = livestock_id
        self.disease_name = disease_name
