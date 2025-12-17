from fastapi import APIRouter, HTTPException
from security.device_guard import is_device_allowed

router = APIRouter()

@router.post("/telemetry")
async def ingest_telemetry(payload: TelemetryPayload):
    if not is_device_allowed(payload.deviceId):
        raise HTTPException(
            status_code=403,
            detail="Device not approved",
        )

    # ✅ safe to store
    save_telemetry(payload)
    return {"status": "ok"}
