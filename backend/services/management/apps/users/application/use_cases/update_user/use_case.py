from apps.users.application.use_cases.update_user.input_dto import UpdateUserInputDTO
from apps.users.application.use_cases.update_user.output_dto import UpdateUserOutputDTO


class UpdateUserUseCase:
    def execute(self, input_dto: UpdateUserInputDTO) -> UpdateUserOutputDTO:
        raise NotImplementedError
