from rest_framework import serializers

from apps.users.application.use_cases.create_user.input_dto import CreateUserInputDTO
from apps.users.application.use_cases.create_user.output_dto import CreateUserOutputDTO
from shared.schemas.create_user.create_user_input import CreateUserInputSchema
from shared.schemas.create_user.create_user_output import CreateUserOutputSchema


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    is_staff = serializers.BooleanField(required=False, default=False)
    is_superuser = serializers.BooleanField(required=False, default=False)

    @staticmethod
    def to_input_dto(data: dict) -> CreateUserInputDTO:
        schema = CreateUserInputSchema(
            email=data["email"],
            password=data["password"],
            phone_number=data.get("phone_number", ""),
            is_staff=data.get("is_staff", False),
            is_superuser=data.get("is_superuser", False),
        )
        return CreateUserInputDTO(**schema.__dict__)

    @staticmethod
    def to_output_schema(output_dto: CreateUserOutputDTO) -> CreateUserOutputSchema:
        return CreateUserOutputSchema(id=output_dto.id, email=output_dto.email)
