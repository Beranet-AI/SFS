from ..application.use_cases.execute_command.output_dto import (
    BaseCommandResultDTO,
)
from ..application.use_cases.send_result.input_dto import SendResultInputDTO
from ..application.use_cases.send_result.output_dto import SendResultOutputDTO


class InboundResultMapper:
    @staticmethod
    def to_input(dto: BaseCommandResultDTO) -> SendResultInputDTO:
        return SendResultInputDTO(
            command_id=dto.command_id,
            command_type=dto.command_type,
            status=dto.status,
            executed_at=dto.executed_at,
            payload=dto.__dict__,
        )


class OutboundResultMapper:
    @staticmethod
    def to_response(dto: SendResultOutputDTO) -> dict:
        return {"delivered": dto.delivered}
