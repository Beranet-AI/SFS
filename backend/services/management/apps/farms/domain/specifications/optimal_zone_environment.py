class OptimalZoneEnvironment:
    def is_satisfied_by(self, metrics) -> bool:
        return (
            18 <= metrics.temperature <= 26
            and metrics.humidity < 70
            and metrics.ammonia < 10
        )
