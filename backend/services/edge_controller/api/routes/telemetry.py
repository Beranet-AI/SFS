# api/routes/telemetry.py
from fastapi import APIRouter, HTTPException, status
from .base import router as base_router

from ...application.edge_service import EdgeService
from ...mappers.telemetry_mapper import raw_telemetry_to_dto

from ...validators.telemetry_validator import validate_telemetry_payload            # 0️⃣ Schema validation

  
router = APIRouter(
    prefix="/telemetry",
    tags=["telemetry"]
)

edge_service = EdgeService()


@router.post(
    "",
    summary="Receive telemetry from device",
    description="Forward telemetry from approved devices to data_ingestion"
)
def receive_telemetry(payload: dict):
    try:

        # 0️⃣ Schema validation
        validate_telemetry_payload(payload)

        telemetry_dto = raw_telemetry_to_dto(
            edge_id=payload["edge_id"],
            device_id=payload["device_id"],
            device_type=payload["device_type"],
            metrics=payload["metrics"],
            meta=payload.get("meta"),
        )

        edge_service.handle_telemetry(telemetry_dto)

        return {"status": "FORWARDED"}

    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing field: {str(e)}",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Telemetry forwarding failed: {str(e)}",
        )


base_router.include_router(router)
