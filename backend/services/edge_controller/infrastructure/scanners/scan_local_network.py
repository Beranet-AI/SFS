# infrastructure/scanners/scan_local_network.py

from .subnet_resolver import resolve_subnets
from .arp_scan import arp_scan
from .ping_probe import ping_probe
from .tcp_probe import tcp_probe
from .classifier import classify_device
from .payload_builder import build_device_payload


def scan_local_network():
    """
    Full discovery pipeline
    """
    discovered_devices = []

    subnets = resolve_subnets()

    for subnet in subnets:
        layer2_devices = arp_scan(subnet)

        for dev in layer2_devices:
            if not ping_probe(dev["ip"]):
                continue

            open_ports = tcp_probe(dev["ip"])
            device_type = classify_device(dev, open_ports)

            payload = build_device_payload(
                dev,
                open_ports,
                device_type
            )

            discovered_devices.append(payload)

    return discovered_devices
