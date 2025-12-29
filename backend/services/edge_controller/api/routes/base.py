# api/routes/base.py

from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=["edge-controller"]
)
