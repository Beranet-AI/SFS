import logging

logger = logging.getLogger("EdgeControllerClient")


class EdgeControllerClient:
    def approve_device(self, device_id: str) -> None:
        logger.info(f"[EDGE CONTROLLER] Approved device: {device_id}")
