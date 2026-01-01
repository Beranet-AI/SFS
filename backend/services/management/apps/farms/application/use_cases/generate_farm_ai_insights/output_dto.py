
from dataclasses import dataclass

@dataclass
class GenerateFarmAIInsightsOutputDTO:
    farm_id: str
    insights: list[dict]
    