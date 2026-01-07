from apps.commands.application.services.command_dispatcher import CommandDispatcher
from apps.commands.domain.domain_services.command_policy import CommandPolicy
from apps.commands.domain.enums.command_status import CommandStatus
from apps.commands.domain.enums.command_type import CommandType
from apps.commands.domain.exceptions.command_execution_error import (
    CommandExecutionError,
)
from apps.commands.domain.exceptions.invalid_target import InvalidTargetError
from apps.commands.domain.exceptions.unsupported_command import (
    UnsupportedCommandError,
)
from apps.commands.domain.repositories.capability_repository import (
    CapabilityRepository,
)
from apps.commands.domain.repositories.command_repository import CommandRepository
from apps.commands.domain.specifications.is_command_allowed import IsCommandAllowed
from .input_dto import SendCommandInputDTO
from .output_dto import SendCommandOutputDTO


class SendCommandUseCase:
    def __init__(
        self,
        *,
        repository: CommandRepository,
        dispatcher: CommandDispatcher,
        capability_repository: CapabilityRepository,
    ) -> None:
        self._repository = repository
        self._dispatcher = dispatcher
        self._policy = CommandPolicy(capability_repository=capability_repository)
        self._is_command_allowed = IsCommandAllowed(
            capability_repository=capability_repository
        )

    def execute(self, dto: SendCommandInputDTO, *, created_by: str) -> SendCommandOutputDTO:
        command_name = dto.command_name.strip()
        if not command_name:
            raise UnsupportedCommandError("command_name is required")
        if not dto.target_kind.strip():
            raise InvalidTargetError("target_kind is required")
        if not dto.target_id.strip():
            raise InvalidTargetError("target_id is required")

        if dto.ack_deadline_sec is not None and dto.ack_deadline_sec <= 0:
            raise CommandExecutionError("ack_deadline_sec must be positive")
        if dto.result_deadline_sec is not None and dto.result_deadline_sec <= 0:
            raise CommandExecutionError("result_deadline_sec must be positive")
        if dto.max_attempts is not None and dto.max_attempts <= 0:
            raise CommandExecutionError("max_attempts must be positive")

        command_type = dto.command_type or command_name
        if (
            command_name == CommandType.GET_CONNECTED_DEVICES.value
            and command_type == command_name
        ):
            command_type = CommandType.DISCOVER.value
        if dto.device_category and dto.device_type:
            self._is_command_allowed.validate(
                command_type=command_type,
                device_category=dto.device_category,
                device_type=dto.device_type,
            )

        data = self._policy.apply(
            command_name=command_name,
            target_kind=dto.target_kind,
            target_id=dto.target_id,
            edge_node_id=dto.edge_node_id,
            payload=dto.payload,
            idempotency_key=dto.idempotency_key,
            ack_deadline_sec=dto.ack_deadline_sec,
            result_deadline_sec=dto.result_deadline_sec,
            max_attempts=dto.max_attempts,
            command_type=command_type,
            device_category=dto.device_category,
            device_type=dto.device_type,
        )
        command = self._repository.create(data=data, created_by=created_by)

        edge_id = command.edge_node_id or command.target_id
        outgoing_payload = {
            "command_id": str(command.id),
            "command_type": command_type,
            "edge_id": edge_id,
            "issued_at": command.created_at.isoformat(),
            "payload": command.payload,
        }
        self._dispatcher.dispatch(
            command=outgoing_payload,
            edge_id=edge_id,
            device_category=dto.device_category,
            device_type=dto.device_type,
            command_type=command_type,
        )
        self._repository.mark_dispatched(command_id=command.id)

        return SendCommandOutputDTO(
            command_id=str(command.id),
            status=CommandStatus.DISPATCHED,
            command_name=command.command_name,
            target_kind=command.target_kind,
            target_id=command.target_id,
            edge_node_id=edge_id,
        )
