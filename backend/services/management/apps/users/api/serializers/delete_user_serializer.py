from rest_framework import serializers

from apps.users.application.use_cases.delete_user.input_dto import DeleteUserInputDTO
from apps.users.application.use_cases.delete_user.output_dto import DeleteUserOutputDTO
from shared.schemas.delete_user.delete_user_input import DeleteUserInputSchema
from shared.schemas.delete_user.delete_user_output import DeleteUserOutputSchema


class DeleteUserSerializer(serializers.Serializer):
    user_id = serializers.CharField()

    @staticmethod
    def to_input_dto(data: dict) -> DeleteUserInputDTO:
        schema = DeleteUserInputSchema(user_id=data["user_id"])
        return DeleteUserInputDTO(**schema.__dict__)

    @staticmethod
    def to_output_schema(output_dto: DeleteUserOutputDTO) -> DeleteUserOutputSchema:
        return DeleteUserOutputSchema(user_id=output_dto.user_id, deleted=output_dto.deleted)
