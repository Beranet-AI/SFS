from __future__ import annotations

from datetime import datetime

from backend.services.monitoring.domain.device_health_state import DeviceHealthState, utcnow
from backend.services.monitoring.domain.enums import DeviceHealth
from backend.shared.dto.health_status_dto import HeartbeatInDTO, HealthSnapshotDTO
from backend.services.monitoring.infrastructure.repositories.heartbeat_repository import HeartbeatRepository
from backend.services.monitoring.application.dispatchers.incident_dispatcher import IncidentDispatcher


class DeviceHealthService:
    def __init__(
        self,
        heartbeat_repo: HeartbeatRepository,
        incident_dispatcher: IncidentDispatcher,
        offline_threshold_seconds: int,
    ) -> None:
        self.repo = heartbeat_repo
        self.incidents = incident_dispatcher
        self.offline_threshold_seconds = offline_threshold_seconds

    async def register_heartbeat(self, hb: HeartbeatInDTO) -> HealthSnapshotDTO:
        now = utcnow()
        state = await self.repo.get_or_create(hb.device_id, now)
        state.mark_seen(now)
        await self.repo.save(state)
        return self._snapshot(state)

    async def get_health_snapshot(self, device_id: str) -> HealthSnapshotDTO:
        state = await self.repo.get(device_id)
        if state is None:
            # unknown device → treat as offline/unknown
            return HealthSnapshotDTO(
                device_id=device_id,
                health=DeviceHealth.OFFLINE.value,
                last_seen_at=None,
                server_time=utcnow().isoformat(),
            )
        return self._snapshot(state)

    async def offline_check_tick(self) -> None:
        now = utcnow()
        all_states = await self.repo.list_all()
        for st in all_states:
            prev = st.health
            became_offline = st.evaluate_offline(self.offline_threshold_seconds, now=now)
            if became_offline and prev != DeviceHealth.OFFLINE:
                await self.repo.save(st)
                await self.incidents.device_offline(
                    device_id=st.device_id,
                    last_seen_at_iso=st.last_seen_at.isoformat(),
                )

    def _snapshot(self, st: DeviceHealthState) -> HealthSnapshotDTO:
        return HealthSnapshotDTO(
            device_id=st.device_id,
            health=st.health.value,
            last_seen_at=st.last_seen_at.isoformat() if isinstance(st.last_seen_at, datetime) else None,
            server_time=utcnow().isoformat(),
        )
