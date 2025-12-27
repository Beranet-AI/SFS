from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from datetime import datetime

from backend.services.monitoring.domain.device_health_state import DeviceHealthState


class HeartbeatRepository(ABC):
    @abstractmethod
    async def get(self, device_id: str) -> Optional[DeviceHealthState]:
        raise NotImplementedError

    @abstractmethod
    async def get_or_create(self, device_id: str, now: datetime) -> DeviceHealthState:
        raise NotImplementedError

    @abstractmethod
    async def save(self, state: DeviceHealthState) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> List[DeviceHealthState]:
        raise NotImplementedError


class InMemoryHeartbeatRepository(HeartbeatRepository):
    def __init__(self) -> None:
        self._store: Dict[str, DeviceHealthState] = {}

    async def get(self, device_id: str) -> Optional[DeviceHealthState]:
        return self._store.get(device_id)

    async def get_or_create(self, device_id: str, now: datetime) -> DeviceHealthState:
        st = self._store.get(device_id)
        if st is None:
            st = DeviceHealthState(device_id=device_id, last_seen_at=now)
            self._store[device_id] = st
        return st

    async def save(self, state: DeviceHealthState) -> None:
        self._store[state.device_id] = state

    async def list_all(self) -> List[DeviceHealthState]:
        return list(self._store.values())
