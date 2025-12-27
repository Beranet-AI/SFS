from discovery.scan_local_network import ScanLocalNetworkUseCase
from .execute_device_command import ExecuteDeviceCommandUseCase


def dispatch_command(command: dict):
    cmd = command.get("command")

    if cmd == "scan_network":
        ScanLocalNetworkUseCase(
            edge_id=command["edge_id"]
        ).execute()

    elif cmd == "device_command":
        ExecuteDeviceCommandUseCase().execute(command)

    else:
        print("Unknown command:", cmd)
