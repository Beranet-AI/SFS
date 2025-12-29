# infrastructure/scanners/payload_builder.py

def build_device_payload(device, open_ports, device_type):
    return {
        "device_serial": device["mac"],
        "ip_address": device["ip"],
        "protocols": open_ports,
        "device_type": device_type,
        "capabilities": {
            "telemetry": device_type.endswith("SENSOR"),
            "command": device_type.endswith("CONTROLLER"),
        }
    }
