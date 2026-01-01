# File: farm/domain/domain_services/environment_analyzer.py
class EnvironmentAnalyzer:
    def thi(self, temperature_c: float, humidity: float) -> float:
        # THI ساده (نسخه صنعتی دقیق‌تر می‌شود)
        return (1.8 * temperature_c + 32) - (0.55 - 0.0055 * humidity) * (1.8 * temperature_c - 26)

    def risk_level(self, temperature_c: float, humidity: float) -> str:
        thi = self.thi(temperature_c, humidity)
        if thi >= 80: return "HIGH"
        if thi >= 72: return "MEDIUM"
        return "NORMAL"
