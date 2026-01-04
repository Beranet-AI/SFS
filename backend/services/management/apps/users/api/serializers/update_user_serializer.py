from rest_framework import serializers

from apps.users.application.use_cases.update_user.input_dto import UpdateUserInputDTO
from apps.users.application.use_cases.update_user.output_dto import UpdateUserOutputDTO
from shared.schemas.update_user.update_user_input import UpdateUserInputSchema
from shared.schemas.update_user.update_user_output import UpdateUserOutputSchema


class UpdateUserSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    email = serializers.EmailField(required=False, allow_blank=False)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False)
    is_active_account = serializers.BooleanField(required=False)
    is_staff = serializers.BooleanField(required=False)
    is_superuser = serializers.BooleanField(required=False)

    @staticmethod
    def to_input_dto(data: dict) -> UpdateUserInputDTO:
        schema = UpdateUserInputSchema(
            user_id=data["user_id"],
            email=data.get("email"),
            phone_number=data.get("phone_number"),
            is_active=data.get("is_active"),
            is_active_account=data.get("is_active_account"),
            is_staff=data.get("is_staff"),
            is_superuser=data.get("is_superuser"),
        )
        return UpdateUserInputDTO(**schema.__dict__)

    @staticmethod
    def to_output_schema(output_dto: UpdateUserOutputDTO) -> UpdateUserOutputSchema:
        return UpdateUserOutputSchema(id=output_dto.id, email=output_dto.email)
