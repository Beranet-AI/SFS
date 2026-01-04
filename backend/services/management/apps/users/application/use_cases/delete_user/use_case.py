from apps.users.application.use_cases.delete_user.input_dto import DeleteUserInputDTO
from apps.users.application.use_cases.delete_user.output_dto import DeleteUserOutputDTO
from apps.users.domain.repositories.user_repo import UserRepository


class DeleteUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def execute(self, input_dto: DeleteUserInputDTO) -> DeleteUserOutputDTO:
        deleted = self._repository.delete(input_dto.user_id)
        return DeleteUserOutputDTO(user_id=input_dto.user_id, deleted=deleted)
