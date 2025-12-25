from rest_framework import serializers
from apps.control.models import CommandModel

class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandModel
        fields = "__all__"
