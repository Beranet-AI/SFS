from ...core.logging import get_logger

logger = get_logger("ManagementTelemetryClient")


class ManagementTelemetryClient:
    def send_raw_telemetry(self, payload: dict) -> None:
        logger.info(f"[MANAGEMENT TELEMETRY] Raw telemetry sent: {payload}")
