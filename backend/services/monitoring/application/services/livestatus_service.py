from typing import Dict, Any, Optional
from collections import defaultdict, deque


class LiveStatusService:
    """
    Very lightweight in-memory store for realtime dashboard.
    In production: replace with Redis pubsub / NATS / Kafka.
    """
    def __init__(self):
        self._by_livestock = defaultdict(lambda: deque(maxlen=200))
        self._by_device = defaultdict(lambda: deque(maxlen=200))

    def add(self, evt: Dict[str, Any]) -> None:
        livestock_id = evt.get("livestock_id")
        device_serial = evt.get("device_serial") or evt.get("serial")

        if livestock_id:
            self._by_livestock[livestock_id].append(evt)
        if device_serial:
            self._by_device[device_serial].append(evt)

    def get_recent(self, livestock_id: Optional[str] = None, device_serial: Optional[str] = None):
        if livestock_id:
            return list(self._by_livestock[livestock_id])
        if device_serial:
            return list(self._by_device[device_serial])
        return []
