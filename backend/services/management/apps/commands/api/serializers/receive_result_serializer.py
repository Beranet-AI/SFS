from rest_framework import serializers

from apps.commands.application.use_cases.receive_result.input_dto import (
    ReceiveResultInputDTO,
)
from apps.commands.application.use_cases.receive_result.output_dto import (
    ReceiveResultOutputDTO,
)
from apps.commands.domain.enums.command_status import CommandStatus


class ReceiveResultSerializer(serializers.Serializer):
    command_id = serializers.UUIDField()
    attempt_no = serializers.IntegerField(min_value=1)
    status = serializers.ChoiceField(
        choices=[(status.value, status.value) for status in CommandStatus]
    )
    result = serializers.JSONField(required=False)
    error_code = serializers.CharField(max_length=64, required=False, allow_blank=True)
    error_message = serializers.CharField(required=False, allow_blank=True)
    meta = serializers.JSONField(required=False)

    def to_input_dto(self) -> ReceiveResultInputDTO:
        payload = {
            **self.validated_data,
            "command_id": str(self.validated_data["command_id"]),
            "result": self.validated_data.get("result") or {},
            "error_code": self.validated_data.get("error_code") or "",
            "error_message": self.validated_data.get("error_message") or "",
            "meta": self.validated_data.get("meta") or {},
        }
        return ReceiveResultInputDTO(**payload)

    @staticmethod
    def to_output_dto() -> ReceiveResultOutputDTO:
        return ReceiveResultOutputDTO(ok=True)

    @staticmethod
    def to_response() -> dict:
        return {"ok": True}
