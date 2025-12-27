from .subnet_resolver import resolve_local_subnet
from .arp_scan import arp_scan
from .tcp_probe import probe_port
from .payload_builder import build_payload
from .reporter import report

PORTS = [502, 4840, 80, 443]


class ScanLocalNetworkUseCase:

    def __init__(self, *, edge_id: str):
        self.edge_id = edge_id

    def execute(self):
        _, network = resolve_local_subnet()
        hosts = arp_scan()

        for ip, mac in hosts:
            open_ports = [p for p in PORTS if probe_port(ip, p)]
            payload = build_payload(
                edge_id=self.edge_id,
                ip=ip,
                mac=mac,
                open_ports=open_ports,
            )
            report(payload)
