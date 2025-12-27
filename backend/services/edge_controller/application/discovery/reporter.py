from infrastructure.mqtt.client import EdgeMQTTClient

_mqtt = None


def init_mqtt(edge_id: str):
    global _mqtt
    _mqtt = EdgeMQTTClient(edge_id=edge_id)


def report(payload: dict):
    if _mqtt:
        _mqtt.publish_discovery_result(payload)
    else:
        print("[DISCOVERY RESULT]", payload)
