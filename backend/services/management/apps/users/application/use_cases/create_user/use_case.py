from apps.users.application.use_cases.create_user.input_dto import CreateUserInputDTO
from apps.users.application.use_cases.create_user.output_dto import CreateUserOutputDTO
from apps.users.domain.entities.user import User
from apps.users.domain.repositories.user_repo import UserRepository
from apps.users.domain.value_objects.email import Email


class CreateUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def execute(self, input_dto: CreateUserInputDTO) -> CreateUserOutputDTO:
        user = User(
            id=None,
            email=Email(input_dto.email),
            phone_number=input_dto.phone_number,
            is_staff=input_dto.is_staff,
            is_superuser=input_dto.is_superuser,
            is_active=True,
            is_active_account=True,
        )
        created_user = self._repository.create(user, password=input_dto.password)
        return CreateUserOutputDTO(
            id=str(created_user.id),
            email=created_user.email.value,
        )
