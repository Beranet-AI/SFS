# backend/services/management/apps/shared/api/base.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Base(APIView):
    """
    Base HTTP controller (adapter).
    """

    request_serializer_class = None
    response_serializer_class = None

    def get_request_serializer(self, *args, **kwargs):
        if not self.request_serializer_class:
            raise NotImplementedError(
                "request_serializer_class is not defined"
            )
        return self.request_serializer_class(*args, **kwargs)

    def get_response_serializer(self, *args, **kwargs):
        if not self.response_serializer_class:
            raise NotImplementedError(
                "response_serializer_class is not defined"
            )
        return self.response_serializer_class(*args, **kwargs)

    def validate_request(self, request):
        serializer = self.get_request_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def success(self, data, http_status=status.HTTP_200_OK):
        serializer = self.get_response_serializer(data)
        return Response(serializer.data, status=http_status)

    @property
    def user_id(self):
        user = getattr(self.request, "user", None)
        return getattr(user, "id", None)
