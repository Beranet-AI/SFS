class FarmRequiresIntervention:
    def is_satisfied_by(self, economic_metrics) -> bool:
        return economic_metrics.profit < 0
