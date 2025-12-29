# infrastructure/scanners/tcp_probe.py

import socket

COMMON_PORTS = [22, 80, 443, 1883, 502, 8080]


def tcp_probe(ip: str):
    open_ports = []

    for port in COMMON_PORTS:
        try:
            with socket.create_connection((ip, port), timeout=0.5):
                open_ports.append(port)
        except Exception:
            continue

    return open_ports
