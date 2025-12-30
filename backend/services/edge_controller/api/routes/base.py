# api/routes/base.py

from fastapi import APIRouter

from ...application.services.edge_service import EdgeService


class BaseController:
    """HTTP-independent controller base with shared dependencies."""

    def __init__(self, edge_service: EdgeService | None = None):
        self._edge_service = edge_service or EdgeService()

router = APIRouter(
    prefix="",
    tags=["edge-controller"]
)
