from apps.livestock.domain.rules.health_rules import HealthRules

class UpdateHealthUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, livestock_id: str, score: float):
        livestock = self.repo.get_by_id(livestock_id)
        livestock.update_health(HealthRules.from_score(score))
        self.repo.save(livestock)
        return livestock
