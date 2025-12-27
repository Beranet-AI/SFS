import socket
import ipaddress


def resolve_local_subnet():
    """
    Detect local IP and subnet based on edge machine network.
    Assumes /24 LAN (safe default for Windows LANs).
    """
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    network = ipaddress.ip_network(f"{local_ip}/24", strict=False)
    return local_ip, network
