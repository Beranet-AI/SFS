from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from typing import Dict, Any, Optional

from apps.monitoring.application.services.livestatus_service import LiveStatusService
from apps.monitoring.application.streams.livestatus_event_stream import LiveStatusEventStream

router = APIRouter(prefix="/monitoring", tags=["monitoring"])

_live = LiveStatusService()
_stream = LiveStatusEventStream()


@router.post("/livestatus/push")
async def push_livestatus(payload: Dict[str, Any]):
    _live.add(payload)
    await _stream.publish(payload)
    return {"ok": True}


@router.get("/livestatus/recent")
def recent(livestock_id: Optional[str] = None, device_serial: Optional[str] = None):
    return _live.get_recent(livestock_id=livestock_id, device_serial=device_serial)


@router.get("/livestatus/stream")
def stream(request: Request, livestock_id: Optional[str] = None):
    return StreamingResponse(
        _stream.subscribe(request, livestock_id=livestock_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


health = DeviceHealthService()


@router.post("/health/heartbeat")
async def heartbeat(payload: dict):
    """
    payload:
    {
      "device_serial": "SENSOR-123",
      "ts": "2025-01-01T12:00:00Z"
    }
    """
    await health.on_heartbeat(payload)
    return {"ok": True}