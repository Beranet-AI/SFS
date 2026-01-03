from apps.users.application.services.users_service import CreateUserService
from apps.users.application.use_cases.create_user.input_dto import CreateUserInputDTO
from apps.users.application.use_cases.create_user.output_dto import CreateUserOutputDTO


class CreateUserUseCase:
    def __init__(self, service: CreateUserService | None = None) -> None:
        self._service = service or CreateUserService()

    def execute(self, input_dto: CreateUserInputDTO) -> CreateUserOutputDTO:
        user = self._service.create_user(
            email=input_dto.email,
            password=input_dto.password,
            phone_number=input_dto.phone_number,
            is_staff=input_dto.is_staff,
            is_superuser=input_dto.is_superuser,
        )
        return CreateUserOutputDTO(id=str(user.id), email=user.email)
