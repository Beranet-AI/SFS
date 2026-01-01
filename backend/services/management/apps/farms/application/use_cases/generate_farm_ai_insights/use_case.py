# farm/application/use_cases/generate_farm_ai_insights/use_case.py
class GenerateFarmAIInsightsUseCase:
    def __init__(self, repo, ai_adapter):
        self.repo = repo
        self.ai = ai_adapter

    def execute(self, dto):
        farm = self.repo.get_by_id(dto.farm_id)
        return self.ai.analyze_farm(farm)
