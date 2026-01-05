from dataclasses import dataclass


@dataclass
class StartNetworkScanOutputDTO:
    scan_id: str
    command_id: str
