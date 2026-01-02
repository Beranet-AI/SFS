# File: livestock/application/use_cases/generate_livestock_ai_insights/input_dto.py
from dataclasses import dataclass

@dataclass
class GenerateLivestockAIInsightsInputDTO:
    livestock_id: str
