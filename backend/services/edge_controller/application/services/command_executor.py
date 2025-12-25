from typing import Dict, Any
import time


class CommandExecutor:
    """
    Executes commands on real hardware (or LabVIEW).
    For now: mock execution.
    """

    def execute(self, command: Dict[str, Any]) -> Dict[str, Any]:
        # Here you will later:
        # - send to LabVIEW
        # - Modbus write
        # - OPC UA call
        # - MQTT publish

        # MOCK:
        time.sleep(0.2)

        return {
            "status": "acked",
            "result": {
                "message": "Command executed successfully",
                "echo": command,
            },
        }
