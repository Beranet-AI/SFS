from apps.commands.application.use_cases.receive_result.input_dto import (
    ReceiveResultInputDTO,
)
from apps.commands.application.use_cases.receive_result.output_dto import (
    ReceiveResultOutputDTO,
)


class ReceiveResultSerializer:
    @staticmethod
    def to_input_dto(data: dict) -> ReceiveResultInputDTO:
        payload = {
            **data,
            "command_id": str(data["command_id"]),
            "result": data.get("result") or {},
            "error_code": data.get("error_code") or "",
            "error_message": data.get("error_message") or "",
            "meta": data.get("meta") or {},
        }
        return ReceiveResultInputDTO(**payload)

    @staticmethod
    def to_output_dto() -> ReceiveResultOutputDTO:
        return ReceiveResultOutputDTO(ok=True)

    @staticmethod
    def to_response() -> dict:
        return {"ok": True}
