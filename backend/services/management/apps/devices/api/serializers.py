from rest_framework import serializers

class DeviceSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    serial = serializers.CharField()
    device_type = serializers.CharField()
    status = serializers.CharField()
    assigned_livestock_id = serializers.CharField(allow_null=True)
