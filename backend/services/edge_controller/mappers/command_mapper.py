from datetime import datetime

from ..application.use_cases.execute_command.input_dto import (
    ExecuteCommandInputDTO,
)


def json_to_command_dto(payload: dict) -> ExecuteCommandInputDTO:
    """
    Convert incoming JSON command to ExecuteCommandInputDTO
    """

    try:
        return ExecuteCommandInputDTO(
            command_id=payload["command_id"],
            command_type=payload["command_type"],
            payload=payload.get("payload", {}),
            received_at=datetime.utcnow(),
        )

    except KeyError as e:
        raise ValueError(f"Missing required command field: {e}")
