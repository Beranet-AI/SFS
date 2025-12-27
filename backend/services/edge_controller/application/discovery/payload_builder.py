from datetime import datetime


def build_payload(
    *,
    edge_id: str,
    ip: str,
    mac: str,
    protocol: str,
    open_ports: list[int],
):
    return {
        "edge_id": edge_id,
        "device_serial": f"MAC:{mac}" if mac else f"IP:{ip}",
        "device_type": "unknown",
        "protocol": protocol,
        "ip_address": ip,
        "manufacturer": "",
        "model": "",
        "firmware": "",
        "capabilities": {},
        "raw_payload": {
            "scan_method": "arp+ping+tcp",
            "open_ports": open_ports,
            "mac": mac,
        },
        "last_seen_at": datetime.utcnow().isoformat() + "Z",
    }
