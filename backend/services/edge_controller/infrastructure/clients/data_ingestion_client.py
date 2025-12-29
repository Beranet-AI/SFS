from ...core.logging import get_logger

logger = get_logger("DataIngestionClient")

class DataIngestionClient:
    def send_telemetry(self, payload: dict):
        logger.info(f"[DATA INGESTION] Telemetry sent: {payload}")
