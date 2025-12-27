import subprocess
import re


def arp_scan():
    """
    Reads Windows ARP table (arp -a).
    Returns list of (ip, mac).
    """
    result = subprocess.check_output(
        "arp -a",
        shell=True,
        stderr=subprocess.DEVNULL
    ).decode(errors="ignore")

    hosts = []
    for line in result.splitlines():
        match = re.search(
            r"(\d+\.\d+\.\d+\.\d+)\s+([a-fA-F0-9:-]{17})",
            line
        )
        if match:
            ip, mac = match.groups()
            hosts.append((ip, mac))

    return hosts
