from .report_command_result import report_command_result


class ExecuteDeviceCommandUseCase:
    """
    Executes actuator commands (fan / valve / ozone).
    """

    def execute(self, command: dict):
        device_id = command["device_id"]
        action = command["action"]

        # --- Stub hardware interaction ---
        success = True
        status = "EXECUTED" if success else "FAILED"

        report_command_result(
            command_id=command["command_id"],
            device_id=device_id,
            status=status,
        )
