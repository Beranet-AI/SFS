# infrastructure/scanners/subnet_resolver.py

import socket
import ipaddress


def resolve_subnets():
    """
    Resolve local /24 subnet using stdlib only
    """
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    network = ipaddress.ip_network(f"{local_ip}/24", strict=False)

    return [str(network)]
