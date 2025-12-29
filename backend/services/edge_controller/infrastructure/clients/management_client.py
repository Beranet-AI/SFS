from ...core.logging import get_logger

logger = get_logger("ManagementClient")

class ManagementClient:
    def send_command_result(self, payload: dict):
        logger.info(f"[MANAGEMENT] Command result sent: {payload}")

        # placeholder: mqtt / http / grpc
