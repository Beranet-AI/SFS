class BarnHeatStressRisk:
    def is_satisfied_by(self, zones) -> bool:
        return any(z.environment.temperature > 30 for z in zones)
