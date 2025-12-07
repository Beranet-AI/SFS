# app/main.py

from __future__ import annotations

import logging
from typing import Any, Dict, Literal, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .django_client import DjangoClientError, post_sensor_reading, sensor_exists


logger = logging.getLogger(__name__)

app = FastAPI(title="SmartFarm Decision Engine")


class SensorReadingIn(BaseModel):
    sensor_id: int
    value: float
    quality: Literal["good", "bad", "suspect"] = "good"
    raw_payload: Optional[Dict[str, Any]] = None


class SensorReadingResponse(BaseModel):
    reading_stored: bool
    django_response: Dict[str, Any]


@app.post("/ingest-reading", response_model=SensorReadingResponse)
async def ingest_reading(reading: SensorReadingIn) -> SensorReadingResponse:
    """
    Endpoint consumed by LabVIEW to forward a fresh sensor reading to Django.
    """

    payload = {
        "sensor_id": reading.sensor_id,
        "value": reading.value,
        "quality": reading.quality,
        "raw_payload": reading.raw_payload or {},
    }

    try:
        if not sensor_exists(reading.sensor_id):
            raise HTTPException(
                status_code=404,
                detail=f"Sensor with id={reading.sensor_id} does not exist in Django.",
            )
        django_response = post_sensor_reading(payload)
    except HTTPException:
        raise
    except DjangoClientError as exc:
        logger.error("Failed to post reading to Django", exc_info=exc)
        raise HTTPException(
            status_code=502,
            detail="Upstream Django service is unavailable or returned an error.",
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return SensorReadingResponse(reading_stored=True, django_response=django_response)

