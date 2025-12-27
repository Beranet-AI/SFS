import uuid


class SendDeviceCommandUseCase:

    def execute(self, *, device_id: str, action: str):
        command = {
            "command": "device_command",
            "command_id": str(uuid.uuid4()),
            "device_id": device_id,
            "action": action,
        }

        # Stub: MQTT / HTTP
        print("[SEND DEVICE COMMAND]", command)

        return command["command_id"]
