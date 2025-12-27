from __future__ import annotations

from backend.services.monitoring.application.dispatchers.command_dispatcher import CommandDispatcher
from backend.services.monitoring.application.dispatchers.incident_dispatcher import IncidentDispatcher
from backend.services.monitoring.application.streams.livestatus_event_stream import LiveStatusEventStream
from backend.shared.dto.livestatus_dto import LiveStatusEventDTO


class LiveStatusService:
    def __init__(
        self,
        stream: LiveStatusEventStream,
        incident_dispatcher: IncidentDispatcher,
        command_dispatcher: CommandDispatcher,
    ) -> None:
        self.stream = stream
        self.incidents = incident_dispatcher
        self.commands = command_dispatcher

    async def publish_livestatus(self, dto: LiveStatusEventDTO) -> None:
        # 1) publish to SSE
        await self.stream.publish(dto)

        # 2) (future) run rules, raise incidents, trigger commands
        #    For now we keep it simple: example threshold hook
        if dto.metric == "temp" and dto.value >= 45:
            await self.incidents.rule_violation(
                rule_code="TEMP_TOO_HIGH",
                device_id=dto.device_id,
                details={"metric": dto.metric, "value": dto.value, "ts": dto.ts},
            )
            # Example auto-actuation (later configurable by rules/policies)
            await self.commands.send_command(
                device_id=dto.device_id,
                command="FAN_ON",
                params={"level": 3},
            )
