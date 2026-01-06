from ...logging import get_logger

logger = get_logger("CommandsClient")


class CommandsClient:
    def send_command_result(self, payload: dict):
        logger.info(f"[COMMANDS] Command result sent: {payload}")

        # placeholder: mqtt / http / grpc
