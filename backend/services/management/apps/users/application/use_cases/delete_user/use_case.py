from apps.users.application.use_cases.delete_user.input_dto import DeleteUserInputDTO
from apps.users.application.use_cases.delete_user.output_dto import DeleteUserOutputDTO


class DeleteUserUseCase:
    def execute(self, input_dto: DeleteUserInputDTO) -> DeleteUserOutputDTO:
        raise NotImplementedError
