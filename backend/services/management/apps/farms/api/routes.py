from fastapi import APIRouter
from .base import ok
from .schemas.environment_metrics import EnvironmentMetricsSchema
from ..domain.value_objects.environmental_metrics import EnvironmentalMetrics

router = APIRouter(prefix="/farms", tags=["farms"])

@router.get("/health")
def health():
    return ok({"service": "farms", "status": "up"})

# نمونهٔ endpoint اسکلت
@router.post("/{farm_id}/{barn_id}/{zone_id}/environment")
def record_env(farm_id: str, barn_id: str, zone_id: str, payload: EnvironmentMetricsSchema):
    metrics = EnvironmentalMetrics(
        temperature=payload.temperature,
        humidity=payload.humidity,
        ammonia=payload.ammonia,
    )
    return ok({"farm_id": farm_id, "barn_id": barn_id, "zone_id": zone_id, "metrics": metrics.__dict__})
