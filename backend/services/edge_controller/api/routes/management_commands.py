from fastapi import APIRouter, HTTPException, status
from .base import BaseController, router as base_router

from ...infrastructure.mappers.command_mapper import (
    InboundCommandMapper,
    OutboundCommandMapper,
)


class CommandController(BaseController):
    """Command controller receiving payloads from CommandsClient."""

    def execute(self, payload: dict) -> dict:
        command_dto = InboundCommandMapper.to_input(payload)
        result_dto = self._edge_service.handle_command(command_dto)
        return OutboundCommandMapper.to_response(result_dto)


router = APIRouter(
    prefix="/api/commands",
    tags=["command"],
)

controller = CommandController()


@router.post(
    "",
    summary="Execute command on edge",
    description="Receive command from management and execute it"
)
def execute_command(payload: dict):
    try:
        return controller.execute(payload)

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
