# File: livestock/domain/specifications/eligible_for_insemination.py
class EligibleForInsemination:
    def is_satisfied_by(self, reproduction) -> bool:
        return bool(reproduction.estrus) and not bool(reproduction.pregnant)
