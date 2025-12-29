from ...core.logging import get_logger

logger = get_logger("MonitoringClient")

class MonitoringClient:
    def send_status(self, payload: dict):
        logger.info(f"[MONITORING] Status sent: {payload}")
