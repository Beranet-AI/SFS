import json
from .dispatch_command import dispatch_command


class ListenCommandsUseCase:
    """
    Entry point for edge commands (MQTT / HTTP consumer).
    """

    def execute(self, *, message: str):
        data = json.loads(message)
        dispatch_command(data)
