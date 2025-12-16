import uuid
from datetime import datetime

import httpx

from backend.services.monitoring.application.event_bus import event_bus
from backend.services.monitoring.domain.live_status import (
    LiveStatusEvent,
    LiveStatusPayload,
    LiveStatusSeverity,
)


MANAGEMENT_INCIDENTS_URL = "http://management:8000/api/v1/incidents/"


async def publish_live_status(
    *,
    metric: str,
    value: float,
    severity: LiveStatusSeverity,
    device_id: str,
    zone_id: str | None = None,
):
    event = LiveStatusEvent(
        id=str(uuid.uuid4()),
        type="LIVE_STATUS_RAISED",
        severity=severity,
        payload=LiveStatusPayload(
            metric=metric,
            value=value,
            deviceId=device_id,
            zoneId=zone_id,
        ),
        timestamp=datetime.utcnow(),
    )

    # 1️⃣ Live → Dashboard
    await event_bus.publish(event)

    # 2️⃣ Durable → Management
    async with httpx.AsyncClient() as client:
        await client.post(
            MANAGEMENT_INCIDENTS_URL,
            json=event.model_dump(),
            timeout=2.0,
        )
