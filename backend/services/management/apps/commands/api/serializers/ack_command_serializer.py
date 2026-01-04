from rest_framework import serializers

from apps.commands.application.use_cases.ack_command.input_dto import (
    AckCommandInputDTO,
)
from apps.commands.application.use_cases.ack_command.output_dto import (
    AckCommandOutputDTO,
)


class AckCommandSerializer(serializers.Serializer):
    command_id = serializers.UUIDField()
    attempt_no = serializers.IntegerField(min_value=1)
    executor_receipt = serializers.CharField(
        max_length=128, required=False, allow_blank=True
    )
    meta = serializers.JSONField(required=False)

    def to_input_dto(self) -> AckCommandInputDTO:
        payload = {
            **self.validated_data,
            "command_id": str(self.validated_data["command_id"]),
        }
        return AckCommandInputDTO(**payload)

    @staticmethod
    def to_output_dto() -> AckCommandOutputDTO:
        return AckCommandOutputDTO(ok=True)

    @staticmethod
    def to_response() -> dict:
        return {"ok": True}
