from rest_framework import serializers

class MedicalRecordSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    livestock_id = serializers.CharField()
    diagnosis = serializers.CharField()
    notes = serializers.CharField()
    recorded_at = serializers.DateTimeField()
