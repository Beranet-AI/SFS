# File: livestock/domain/domain_events/estrus_detected.py
class EstrusDetected:
    def __init__(self, livestock_id: str):
        self.livestock_id = livestock_id
