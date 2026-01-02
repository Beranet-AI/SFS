import logging

logger = logging.getLogger("DataIngestionClient")


class DataIngestionClient:
    def send_telemetry(self, payload: dict) -> None:
        logger.info(f"[DATA INGESTION] Telemetry sent: {payload}")
