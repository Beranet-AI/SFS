from __future__ import annotations

import httpx


class ManagementClient:
    """
    Talks to management service (Source of truth + audit + incidents).
    Endpoints here are placeholders; align with your real DRF routes later.
    """

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    async def create_incident(self, title: str, device_id: str, severity: str, details: dict) -> None:
        url = f"{self.base_url}/api/incidents/"
        payload = {
            "title": title,
            "device_id": device_id,
            "severity": severity,
            "details": details,
        }
        async with httpx.AsyncClient(timeout=5.0) as client:
            # best effort; don't crash monitoring if management is down
            try:
                await client.post(url, json=payload)
            except Exception:
                return
