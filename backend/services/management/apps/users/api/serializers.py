from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    role = serializers.CharField()
    is_active = serializers.BooleanField()
