from apps.commands.application.use_cases.receive_result.input_dto import (
    ReceiveResultInputDTO,
)
from apps.commands.application.use_cases.receive_result.output_dto import (
    ReceiveResultOutputDTO,
)


class InboundResultMapper:
    @staticmethod
    def from_payload(payload: dict) -> ReceiveResultInputDTO:
        return ReceiveResultInputDTO(
            command_id=str(payload["command_id"]),
            attempt_no=payload["attempt_no"],
            status=payload["status"],
            result=payload.get("result", {}),
            error_code=payload.get("error_code", ""),
            error_message=payload.get("error_message", ""),
            meta=payload.get("meta", {}),
        )


class OutboundResultMapper:
    @staticmethod
    def to_response(dto: ReceiveResultOutputDTO) -> dict:
        return {"ok": dto.ok}
