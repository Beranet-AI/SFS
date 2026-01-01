# File: farm/domain/value_objects/economic_metrics.py
from dataclasses import dataclass

@dataclass(frozen=True)
class EconomicMetrics:
    feed_cost: float
    treatment_cost: float
    revenue: float

    @property
    def profit(self) -> float:
        return self.revenue - (self.feed_cost + self.treatment_cost)
