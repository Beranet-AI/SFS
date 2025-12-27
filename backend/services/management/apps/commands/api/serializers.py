from rest_framework import serializers
from apps.commands.models import (
    CommandModel,
    CommandAttemptModel,
    CommandTargetKind,
    CommandStatus,
)


class CommandCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandModel
        fields = [
            "command_name",
            "target_kind",
            "target_id",
            "edge_node_id",
            "payload",
            "idempotency_key",
            "ack_deadline_sec",
            "result_deadline_sec",
            "max_attempts",
            "backoff_sec",
        ]

    def validate_target_kind(self, v):
        allowed = {k for k, _ in CommandTargetKind.choices}
        if v not in allowed:
            raise serializers.ValidationError("invalid target_kind")
        return v


class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandModel
        fields = "__all__"


class CommandAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandAttemptModel
        fields = "__all__"
        read_only_fields = ("status", "retries", "created_at")


class CommandAckSerializer(serializers.Serializer):
    command_id = serializers.UUIDField()
    attempt_no = serializers.IntegerField()
    executor_receipt = serializers.CharField(
        required=False, allow_blank=True, default=""
    )
    meta = serializers.JSONField(required=False, default=dict)


class CommandResultSerializer(serializers.Serializer):
    command_id = serializers.UUIDField()
    attempt_no = serializers.IntegerField()

    status = serializers.ChoiceField(
        choices=[
            CommandStatus.SUCCEEDED,
            CommandStatus.FAILED,
            CommandStatus.TIMED_OUT,
            CommandStatus.CANCELLED,
        ]
    )

    result = serializers.JSONField(required=False, default=dict)
    error_code = serializers.CharField(required=False, allow_blank=True, default="")
    error_message = serializers.CharField(required=False, allow_blank=True, default="")
    meta = serializers.JSONField(required=False, default=dict)
