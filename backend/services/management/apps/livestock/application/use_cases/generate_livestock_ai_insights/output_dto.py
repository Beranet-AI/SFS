# File: livestock/application/use_cases/generate_livestock_ai_insights/output_dto.py
from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class GenerateLivestockAIInsightsOutputDTO:
    livestock_id: str
    risk_score: Optional[float]
    health_score: Optional[float]
    ai: Optional[Dict]
    appetite_change: Optional[str]
    abnormal_milk_drop: Optional[bool]
    treatment_response: Optional[str]
