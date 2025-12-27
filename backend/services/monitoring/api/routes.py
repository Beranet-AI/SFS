from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from backend.services.monitoring.core.config import settings
from backend.services.monitoring.api.sse import sse_stream
from backend.shared.dto.health_status_dto import HeartbeatInDTO, HealthSnapshotDTO
from backend.shared.dto.livestatus_dto import LiveStatusEventDTO
from backend.services.monitoring.application.services.device_health_service import DeviceHealthService
from backend.services.monitoring.application.services.livestatus_service import LiveStatusService
from backend.services.monitoring.application.streams.livestatus_event_stream import LiveStatusEventStream


router = APIRouter(tags=["monitoring"])


def get_device_health(request: Request) -> DeviceHealthService:
    return request.app.state.device_health  # set in lifespan


def get_livestatus_service(request: Request) -> LiveStatusService:
    return request.app.state.livestatus_service  # set in lifespan


def get_livestatus_stream(request: Request) -> LiveStatusEventStream:
    return request.app.state.livestatus_stream  # set in lifespan


@router.get("/health", response_model=dict)
def service_health():
    return {"ok": True, "service": settings.SERVICE_NAME, "env": settings.SERVICE_ENV}


@router.post("/devices/heartbeat", response_model=HealthSnapshotDTO)
async def heartbeat(
    body: HeartbeatInDTO,
    svc: DeviceHealthService = Depends(get_device_health),
):
    # A device/edge sends heartbeat here.
    # We return current health snapshot for convenience.
    snapshot = await svc.register_heartbeat(body)
    return snapshot


@router.get("/devices/{device_id}/health", response_model=HealthSnapshotDTO)
async def device_health(
    device_id: str,
    svc: DeviceHealthService = Depends(get_device_health),
):
    return await svc.get_health_snapshot(device_id=device_id)


@router.post("/livestatus/publish", response_model=dict)
async def publish_livestatus(
    body: LiveStatusEventDTO,
    svc: LiveStatusService = Depends(get_livestatus_service),
):
    # data_ingestion can call this endpoint (or monitoring itself can subscribe later)
    await svc.publish_livestatus(body)
    return {"ok": True}


@router.get("/livestatus/stream")
async def livestatus_stream(request: Request):
    stream = get_livestatus_stream(request)

    async def iterator_factory():
        return stream.subscribe()

    return await sse_stream(
        request=request,
        iterator_factory=iterator_factory,
        event_name="livestatus",
        ping_interval_seconds=settings.SSE_PING_INTERVAL_SECONDS,
    )
