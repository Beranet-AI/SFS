# api/routes/health.py
from fastapi import APIRouter
from datetime import datetime


router = APIRouter(
    prefix="/health",
    tags=["health"]
)


@router.get("", summary="Health check")
def health_check():
    return {
        "status": "OK",
        "service": "edge_controller",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
