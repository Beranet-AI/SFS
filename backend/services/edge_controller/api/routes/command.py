from fastapi import APIRouter, HTTPException, status
from .base import router as base_router

from ...application.edge_service import EdgeService

from ...mappers.command_mapper import (
    InboundCommandMapper,
    OutboundCommandMapper,
)


router = APIRouter(
    prefix="/command",
    tags=["command"]
)

edge_service = EdgeService()


@router.post(
    "",
    summary="Execute command on edge",
    description="Receive command from management and execute it"
)
def execute_command(payload: dict):
    try:
        # 1️⃣ JSON → DTO
        command_dto = InboundCommandMapper.to_input(payload)

        # 2️⃣ Orchestrate
        result_dto = edge_service.handle_command(command_dto)

        # 3️⃣ DTO → JSON
        return OutboundCommandMapper.to_response(result_dto)

    except ValueError as e:
        # Contract / validation error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except Exception as e:
        # Unexpected edge failure
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Edge execution failed: {str(e)}",
        )


# register router
base_router.include_router(router)
