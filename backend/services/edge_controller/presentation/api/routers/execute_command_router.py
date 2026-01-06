from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from ....application.use_cases.execute_command.input_dto import (
    ExecuteCommandInputDTO,
)
from ....application.use_cases.execute_command.use_case import (
    ExecuteCommandUseCase,
)
from ..dependencies.use_cases import get_execute_command_use_case
from ..schemas.execute_command_request import ExecuteCommandRequest
from ..schemas.execute_command_response import ExecuteCommandResponse

router = APIRouter(prefix="/api/commands", tags=["command"])


@router.post(
    "",
    summary="Execute command on edge",
    description="Receive command from management and execute it",
    response_model=ExecuteCommandResponse,
)
def execute_command(
    payload: ExecuteCommandRequest,
    use_case: ExecuteCommandUseCase = Depends(get_execute_command_use_case),
) -> ExecuteCommandResponse:
    try:
        dto = ExecuteCommandInputDTO(
            command_id=payload.command_id,
            command_type=payload.command_type,
            edge_id=payload.edge_id,
            issued_at=payload.issued_at.isoformat().replace("+00:00", "Z"),
            payload=payload.payload,
        )
        result = use_case.execute(dto)

        executed_at = datetime.fromisoformat(
            result.executed_at.replace("Z", "+00:00")
        )

        return ExecuteCommandResponse(
            command_id=result.command_id,
            command_type=result.command_type,
            status=result.status,
            executed_at=executed_at,
            devices=getattr(result, "devices", None),
            device_id=getattr(result, "device_id", None),
            execution_state=getattr(result, "execution_state", None),
            reboot_state=getattr(result, "reboot_state", None),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Edge execution failed: {exc}",
        ) from exc
