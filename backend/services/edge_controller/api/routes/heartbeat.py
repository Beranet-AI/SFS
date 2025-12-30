# api/routes/heartbeat.py
from fastapi import APIRouter
from datetime import datetime


router = APIRouter(
    prefix="/heartbeat",
    tags=["heartbeat"]
)


@router.get("", summary="Heartbeat check")
def heartbeat_check():
    return {
        "status": "OK",
        "service": "edge_controller",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
