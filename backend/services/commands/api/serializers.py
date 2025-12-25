from rest_framework import serializers
from apps.commands.infrastructure.models.command_model import CommandModel


class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandModel
        fields = "__all__"


class CommandCreateSerializer(serializers.Serializer):
    command_type = serializers.CharField()
    target_device_serial = serializers.CharField()
    params = serializers.JSONField(required=False)
    source = serializers.ChoiceField(
        choices=["manual", "ai", "system"],
        default="manual"
    )
