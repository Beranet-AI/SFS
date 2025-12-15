import uuid
from datetime import datetime
import httpx

from backend.services.alerting.domain.events import (
    LiveEvent,
    AlertPayload,
    AlertSeverity,
)
from backend.services.alerting.application.event_bus import event_bus


MANAGEMENT_EVENTS_URL = "http://management:8000/events"


async def raise_alert(
    *,
    metric: str,
    value: float,
    severity: AlertSeverity,
    device_id: str,
    zone_id: str | None = None,
):
    event = LiveEvent(
        id=str(uuid.uuid4()),
        type="ALERT_RAISED",
        severity=severity,
        payload=AlertPayload(
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
            MANAGEMENT_EVENTS_URL,
            json=event.model_dump(),
            timeout=2.0,
        )
