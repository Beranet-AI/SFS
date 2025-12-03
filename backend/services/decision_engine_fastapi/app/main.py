# app/main.py

from __future__ import annotations

from typing import Optional, Dict, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .django_client import post_sensor_reading, sensor_exists


app = FastAPI(title="SmartFarm Decision Engine")


class SensorReadingIn(BaseModel):
    sensor_id: int
    value: float
    quality: str = "good"
    raw_payload: Optional[Dict[str, Any]] = None


@app.post("/ingest-reading")
async def ingest_reading(reading: SensorReadingIn):
    """
    این endpoint توسط LabVIEW صدا زده می‌شود.
    JSON ورودی مثل نمونهٔ زیر است:

    {
      "sensor_id": 1,
      "value": 22.85,
      "quality": "good",
      "raw_payload": {"source": "labview"}
    }
    """

    # نگاشت به فرمت موردنیاز Django (SensorReadingSerializer)
    payload = {
        "sensor_id": reading.sensor_id,            # در Django فیلد اسمش sensor است
        "value": reading.value,
        "quality": reading.quality,
        "raw_payload": reading.raw_payload or {},
        # ts را می‌گذاریم خود Django/Serializer مقداردهی کند (auto_now_add یا default)
    }

    try:
        if not sensor_exists(reading.sensor_id):
            raise HTTPException(
                status_code=400,
                detail=f"Sensor with id={reading.sensor_id} does not exist in Django.",
            )
        django_response = post_sensor_reading(payload)
    except HTTPException:
        raise
    except Exception as exc:
        # هر خطایی در تماس با Django اینجا هندل می‌شود
        raise HTTPException(
            status_code=400,
            detail=f"Error posting reading to Django: {exc}",
        )

    return {
        "reading_stored": True,
        "django_response": django_response,
    }

