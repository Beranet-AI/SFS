from rest_framework import serializers


class ReceiveResultSerializer(serializers.Serializer):
    command_id = serializers.UUIDField()
    attempt_no = serializers.IntegerField(min_value=1)
    status = serializers.CharField()
    result = serializers.JSONField()
    error_code = serializers.CharField(required=False, allow_blank=True, default="")
    error_message = serializers.CharField(
        required=False, allow_blank=True, default=""
    )
    meta = serializers.JSONField(required=False, default=dict)
