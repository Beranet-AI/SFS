from apps.users.application.use_cases.update_user.input_dto import UpdateUserInputDTO
from apps.users.application.use_cases.update_user.output_dto import UpdateUserOutputDTO
from apps.users.domain.repositories.user_repo import UserRepository
from apps.users.domain.value_objects.email import Email


class UpdateUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def execute(self, input_dto: UpdateUserInputDTO) -> UpdateUserOutputDTO:
        fields: dict[str, object] = {}
        if input_dto.email is not None:
            fields["email"] = Email(input_dto.email).value
        if input_dto.phone_number is not None:
            fields["phone_number"] = input_dto.phone_number
        if input_dto.is_active is not None:
            fields["is_active"] = input_dto.is_active
        if input_dto.is_active_account is not None:
            fields["is_active_account"] = input_dto.is_active_account
        if input_dto.is_staff is not None:
            fields["is_staff"] = input_dto.is_staff
        if input_dto.is_superuser is not None:
            fields["is_superuser"] = input_dto.is_superuser

        updated_user = self._repository.update(input_dto.user_id, **fields)
        return UpdateUserOutputDTO(
            id=str(updated_user.id),
            email=updated_user.email.value,
        )
