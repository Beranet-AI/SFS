from fastapi import APIRouter
from .base import ok
from .schemas.health_metrics import HealthMetricsSchema

router = APIRouter(prefix="/livestock", tags=["livestock"])

@router.get("/health")
def health():
    return ok({"service": "livestock", "status": "up"})

@router.post("/{livestock_id}/health")
def record_health(livestock_id: str, payload: HealthMetricsSchema):
    return ok({"livestock_id": livestock_id, "payload": payload.dict()})
