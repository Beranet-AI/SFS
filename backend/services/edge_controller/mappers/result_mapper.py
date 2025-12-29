from ..application.use_cases.execute_command.output_dto import (
    BaseCommandResultDTO,
    DiscoverCommandResultDTO,
    OnOffCommandResultDTO,
    RebootCommandResultDTO,
)


def result_dto_to_json(dto: BaseCommandResultDTO) -> dict:
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
