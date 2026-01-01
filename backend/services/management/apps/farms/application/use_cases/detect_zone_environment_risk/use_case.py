# farm/application/use_cases/detect_zone_environment_risk/use_case.py
class DetectZoneEnvironmentRiskUseCase:
    def __init__(self, repo, analyzer):
        self.repo = repo
        self.analyzer = analyzer

    def execute(self, dto):
        farm = self.repo.get_by_id(dto.farm_id)
        barn = next(b for b in farm.barns if b.id == dto.barn_id)
        zone = next(z for z in barn.zones if z.id == dto.zone_id)

        env = zone.environment
        thi = self.analyzer.thi(env.temperature_c, env.humidity)
        risk = self.analyzer.risk_level(env.temperature_c, env.humidity)

        return {
            "zone_id": zone.id,
            "thi": thi,
            "risk_level": risk,
        }
