from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.application.services.user_service import CreateUserService
from apps.users.api.serializers import CreateUserSerializer


class UsersView(APIView):
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = CreateUserService()
        user = service.create_user(**serializer.validated_data)

        return Response(
            {
                "id": str(user.id),
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )
