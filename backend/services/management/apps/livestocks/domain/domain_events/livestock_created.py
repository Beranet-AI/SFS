# File: livestock/domain/domain_events/livestock_created.py
class LivestockCreated:
    def __init__(self, livestock_id: str):
        self.livestock_id = livestock_id
