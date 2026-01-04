from apps.commands.application.use_cases.ack_command.input_dto import (
    AckCommandInputDTO,
)
from apps.commands.application.use_cases.ack_command.output_dto import (
    AckCommandOutputDTO,
)


class AckCommandSerializer:
    @staticmethod
    def to_input_dto(data: dict) -> AckCommandInputDTO:
        payload = {**data, "command_id": str(data["command_id"])}
        return AckCommandInputDTO(**payload)

    @staticmethod
    def to_output_dto() -> AckCommandOutputDTO:
        return AckCommandOutputDTO(ok=True)

    @staticmethod
    def to_response() -> dict:
        return {"ok": True}
