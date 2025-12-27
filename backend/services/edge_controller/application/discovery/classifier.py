def classify_protocol(open_ports: list[int]) -> str:
    if 502 in open_ports:
        return "modbus"
    if 4840 in open_ports:
        return "opcua"
    if 80 in open_ports or 443 in open_ports:
        return "http"
    if 1883 in open_ports:
        return "mqtt"
    return "unknown"
