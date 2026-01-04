from dataclasses import asdict

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.forms.delete_user_form import DeleteUserForm
from apps.users.api.serializers.delete_user_serializer import DeleteUserSerializer
from apps.users.application.use_cases.delete_user.use_case import DeleteUserUseCase
from apps.users.infrastructure.repositories.users_repo_imp import UsersRepositoryImpl


class DeleteUserView(APIView):
    def delete(self, request, user_id: str):
        form = DeleteUserForm({"user_id": user_id})
        if not form.is_valid():
            raise ValidationError(form.errors)

        serializer = DeleteUserSerializer(data=form.cleaned_data)
        serializer.is_valid(raise_exception=True)

        repository = UsersRepositoryImpl()
        use_case = DeleteUserUseCase(repository)
        input_dto = serializer.to_input_dto(serializer.validated_data)
        output_dto = use_case.execute(input_dto)
        output_schema = serializer.to_output_schema(output_dto)

        return Response(asdict(output_schema), status=status.HTTP_200_OK)
