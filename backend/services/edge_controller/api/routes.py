from fastapi import APIRouter, Header, HTTPException
from typing import Dict, Any, Optional
from edge_controller.core.config import settings
from edge_controller.application.services.discovery_service import DiscoveryService
from edge_controller.application.services.forward_service import ForwardService
from edge_controller.infrastructure.clients.management_client import ManagementClient
from edge_controller.infrastructure.clients.ingestion_client import IngestionClient

router = APIRouter(prefix="/edge", tags=["edge"])

_discovery = DiscoveryService(ManagementClient())
_forward = ForwardService(IngestionClient())


@router.post("/ingress/labview")
def labview_ingress(
    payload: Dict[str, Any],
    x_auth_token: Optional[str] = Header(default=None),
):
    """
    LabVIEW -> edge_controller
    Expected payload examples:
    - discovery ping
    - telemetry event
    """
    if x_auth_token != settings.LABVIEW_INGRESS_AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="unauthorized")

    # discovery part (optional)
    if "serial" in payload and "device_type" in payload:
        _discovery.on_seen({
            "serial": payload["serial"],
            "device_type": payload.get("device_type", "unknown"),
            "protocol": payload.get("protocol", "labview"),
            "display_name": payload.get("display_name", ""),
            "farm_id": payload.get("farm_id"),
            "barn_id": payload.get("barn_id"),
            "zone_id": payload.get("zone_id"),
            "livestock_id": payload.get("livestock_id"),
            "metadata": payload.get("metadata", {}),
        })

    # telemetry part (optional)
    if "metric" in payload and "value" in payload:
        _forward.forward_telemetry(payload)

    return {"ok": True}

from edge_controller.application.services.command_executor import CommandExecutor
from edge_controller.infrastructure.clients.management_client import ManagementClient

_executor = CommandExecutor()
_mgmt = ManagementClient()


@router.post("/commands/execute")
def execute_command(payload: Dict[str, Any]):
    result = _executor.execute(payload)

    # Send ACK back to management
    _mgmt.create_incident({
        # optional: replace with command ack endpoint later
        "code": "COMMAND_ACK",
        "severity": "low",
        "title": "Command executed",
        "description": f"Command {payload.get('command_id')} executed",
        "device_serial": payload.get("target_device_serial"),
        "evidence": result,
    })

    return result
