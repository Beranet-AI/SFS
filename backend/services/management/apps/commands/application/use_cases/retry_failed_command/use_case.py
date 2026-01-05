from apps.commands.application.services.command_dispatcher import CommandDispatcher
from apps.commands.domain.enums.command_status import CommandStatus
from apps.commands.domain.repositories.command_repository import CommandRepository
from .input_dto import RetryFailedCommandInputDTO
from .output_dto import RetryFailedCommandOutputDTO


class RetryFailedCommandUseCase:
    def __init__(
        self,
        *,
        repository: CommandRepository,
        dispatcher: CommandDispatcher,
    ) -> None:
        self._repository = repository
        self._dispatcher = dispatcher

    def execute(self, dto: RetryFailedCommandInputDTO) -> RetryFailedCommandOutputDTO:
        command = self._repository.get(command_id=dto.command_id)
        edge_id = command.edge_node_id or command.target_id
        payload = {
            "command_id": str(command.id),
            "command_type": command.command_name,
            "edge_id": edge_id,
            "issued_at": command.created_at.isoformat(),
            "payload": command.payload,
        }
        self._dispatcher.dispatch(
            command=payload,
            edge_id=edge_id,
            device_category=None,
            device_type=None,
            command_type=command.command_name,
        )
        self._repository.mark_dispatched(command_id=command.id)
        return RetryFailedCommandOutputDTO(
            command_id=str(command.id),
            status=CommandStatus.DISPATCHED.value,
        )
