from dataclasses import asdict

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.forms.update_user_form import UpdateUserForm
from apps.users.api.serializers.update_user_serializer import UpdateUserSerializer
from apps.users.application.use_cases.update_user.use_case import UpdateUserUseCase
from apps.users.infrastructure.repositories.users_repo_imp import UsersRepositoryImpl


class UpdateUserView(APIView):
    def patch(self, request, user_id: str):
        payload = {**request.data, "user_id": user_id}
        form = UpdateUserForm(payload)
        if not form.is_valid():
            raise ValidationError(form.errors)

        serializer = UpdateUserSerializer(data=form.cleaned_data)
        serializer.is_valid(raise_exception=True)

        repository = UsersRepositoryImpl()
        use_case = UpdateUserUseCase(repository)
        input_dto = serializer.to_input_dto(serializer.validated_data)
        output_dto = use_case.execute(input_dto)
        output_schema = serializer.to_output_schema(output_dto)

        return Response(asdict(output_schema), status=status.HTTP_200_OK)
