from fastapi import APIRouter
from monitoring.api.schemas import LiveStatusSchema
from monitoring.application.services.livestatus_service import LiveStatusService
from monitoring.infrastructure.cache.livestatus_store import LiveStatusStore
from monitoring.domain.livestatus import LiveStatus

router = APIRouter()
store = LiveStatusStore()
service = LiveStatusService(store)

@router.post("/livestatus/")
def push_livestatus(payload: LiveStatusSchema):
    status = LiveStatus(
        device_id=payload.device_id,
        livestock_id=payload.livestock_id,
        metric=payload.metric,
        value=payload.value,
        recorded_at=payload.recorded_at,
    )
    service.update(status)
    return {"ok": True}

@router.get("/livestatus/{livestock_id}")
def get_livestatus(livestock_id: str):
    statuses = service.get_by_livestock(livestock_id)
    return [
        {
            "device_id": s.device_id,
            "livestock_id": s.livestock_id,
            "metric": s.metric,
            "value": s.value,
            "recorded_at": s.recorded_at,
        }
        for s in statuses
    ]
