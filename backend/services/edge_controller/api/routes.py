from fastapi import APIRouter
from datetime import datetime

from edge_controller.api.schemas import (
    HeartbeatSchema,
    DiscoverySchema,
    ForwardTelemetrySchema,
)
from edge_controller.infrastructure.registry.edge_registry import EdgeRegistry
from edge_controller.application.services.discovery_service import DiscoveryService
from edge_controller.application.services.forward_service import ForwardService
from edge_controller.infrastructure.clients.ingestion_client import IngestionClient
from edge_controller.domain.discovery_event import DiscoveryEvent

router = APIRouter()

_registry = EdgeRegistry()
_discovery_service = DiscoveryService(_registry)
_forward_service = ForwardService(IngestionClient())

@router.get("/health")
def health():
    return {"ok": True, "service": "edge_controller"}

@router.post("/edge/heartbeat")
def heartbeat(payload: HeartbeatSchema):
    node = _discovery_service.heartbeat(
        node_id=payload.node_id,
        name=payload.name,
        ip=payload.ip,
    )
    return {
        "node_id": node.node_id,
        "name": node.name,
        "ip": node.ip,
        "last_seen": node.last_seen,
        "is_online": node.is_online,
    }

@router.get("/edge/nodes")
def list_nodes():
    nodes = _registry.list()
    return [
        {
            "node_id": n.node_id,
            "name": n.name,
            "ip": n.ip,
            "last_seen": n.last_seen,
            "is_online": n.is_online,
        }
        for n in nodes
    ]

@router.post("/edge/discovery")
def discovery(payload: DiscoverySchema):
    event = DiscoveryEvent(
        node_id=payload.node_id,
        discovered_devices=payload.discovered_devices,
        reported_at=payload.reported_at or datetime.utcnow(),
    )
    return _discovery_service.report_discovery(event)

@router.post("/edge/forward-telemetry")
def forward_telemetry(payload: ForwardTelemetrySchema):
    return _forward_service.forward_telemetry(payload.model_dump())
