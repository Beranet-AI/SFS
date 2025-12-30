from datetime import datetime

from ..application.use_cases.execute_command.input_dto import (
    ExecuteCommandInputDTO,
)
from ..application.use_cases.execute_command.output_dto import (
    BaseCommandResultDTO,
    DiscoverCommandResultDTO,
    OnOffCommandResultDTO,
    RebootCommandResultDTO,
)
from ..validators.command_validator import validate_command_payload


class InboundCommandMapper:
    @staticmethod
    def to_input(payload: dict) -> ExecuteCommandInputDTO:
        """
        Convert incoming JSON command to ExecuteCommandInput
        """
        validate_command_payload(payload)

        try:
            return ExecuteCommandInputDTO(
                command_id=payload["command_id"],
                command_type=payload["command_type"],
                edge_id=payload["edge_id"],
                issued_at=datetime.fromisoformat(
                    payload["issued_at"].replace("Z", "+00:00")
                ),
                payload=payload.get("payload", {}),
            )

        except KeyError as e:
            raise ValueError(f"Missing required command field: {e}")


class OutboundCommandMapper:
    @staticmethod
    def to_response(dto: BaseCommandResultDTO) -> dict:
        """
        Convert command result DTO to JSON according to edge_controller output schema.
        Polymorphic and schema-safe.
        """

        base = {
            "command_id": dto.command_id,
            "command_type": dto.command_type,
            "status": dto.status,
            "executed_at": dto.executed_at.isoformat() + "Z",
        }

        # ------------------------
        # DISCOVER
        # ------------------------
        if isinstance(dto, DiscoverCommandResultDTO):
            base["devices"] = dto.devices
            return base

        # ------------------------
        # ON / OFF
        # ------------------------
        if isinstance(dto, OnOffCommandResultDTO):
            base["device_id"] = dto.device_id
            base["execution_state"] = dto.execution_state
            return base

        # ------------------------
        # REBOOT
        # ------------------------
        if isinstance(dto, RebootCommandResultDTO):
            base["device_id"] = dto.device_id
            base["reboot_state"] = dto.reboot_state
            return base

        # ------------------------
        # SAFETY NET
        # ------------------------
        raise ValueError(
            f"Unsupported command result DTO type: {type(dto).__name__}"
        )
