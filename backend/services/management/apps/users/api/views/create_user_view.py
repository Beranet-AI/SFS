from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from apps.users.api.serializers.create_user_serializer import CreateUserSerializer
from apps.users.application.use_cases.create_user.input_dto import CreateUserInputDTO
from apps.users.application.use_cases.create_user.use_case import CreateUserUseCase


class UsersView(APIView):
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = CreateUserUseCase()
        input_dto = CreateUserInputDTO(**serializer.validated_data)
        output_dto = use_case.execute(input_dto)

        return Response(
            {
                "id": output_dto.id,
                "email": output_dto.email,
            },
            status=status.HTTP_201_CREATED,
        )
