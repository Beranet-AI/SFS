# infrastructure/scanners/arp_scan.py

from scapy.all import ARP, Ether, srp


def arp_scan(subnet: str):
    """
    ARP scan on subnet
    """
    result = []

    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet)
    answered, _ = srp(packet, timeout=2, verbose=False)

    for _, recv in answered:
        result.append({
            "ip": recv.psrc,
            "mac": recv.hwsrc
        })

    return result
