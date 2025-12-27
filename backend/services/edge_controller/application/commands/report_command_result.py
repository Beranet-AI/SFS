from infrastructure.mqtt.client import EdgeMQTTClient

_mqtt = None


def init_mqtt(edge_id: str):
    global _mqtt
    _mqtt = EdgeMQTTClient(edge_id=edge_id)


def report_command_result(*, command_id: str, device_id: str, status: str):
    payload = {
        "command_id": command_id,
        "device_id": device_id,
        "status": status,
    }

    if _mqtt:
        _mqtt.publish_command_result(payload)
    else:
        print("[COMMAND RESULT]", payload)
