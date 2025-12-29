# infrastructure/scanners/classifier.py

def classify_device(device, open_ports):
    """
    Simple heuristic classification
    """
    if 1883 in open_ports:
        return "MQTT_SENSOR"

    if 502 in open_ports:
        return "PLC_CONTROLLER"

    if 80 in open_ports or 443 in open_ports:
        return "HTTP_DEVICE"

    return "UNKNOWN"
