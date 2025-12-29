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
            edge_id=payload["edge_id"],
            issued_at=datetime.fromisoformat(
                payload["issued_at"].replace("Z", "+00:00")
            ),
            payload=payload.get("payload", {}),
        )

    except KeyError as e:
        raise ValueError(f"Missing required command field: {e}")
