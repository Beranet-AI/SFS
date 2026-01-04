from typing import Protocol

from apps.commands.application.use_cases.send_command.input_dto import (
    SendCommandInputDTO,
)
from apps.commands.application.use_cases.send_command.use_case import (
    SendCommandUseCase,
)
from apps.commands.domain.entities.discovery_session import DiscoverySession
from apps.commands.domain.enums.command_target_kind import CommandTargetKind
from apps.commands.domain.enums.command_type import CommandType
from apps.commands.domain.exceptions.command_exceptions import CommandValidationError
from apps.commands.domain.repositories.command_repository import CommandRepository
from apps.commands.domain.repositories.discovery_session_repository import (
    DiscoverySessionRepository,
)
from .input_dto import StartDiscoveryInputDTO


class EdgeControllerClient(Protocol):
    def publish_command(self, *, edge_id: str, command: dict) -> None:
        ...


class StartDiscoveryUseCase:
    """
    Create a discovery session and dispatch the DISCOVER command.

    The command runs asynchronously on the edge controller, and the results are
    later persisted by ReceiveResultUseCase via DiscoveryResultService.
    """

    def __init__(
        self,
        *,
        session_repository: DiscoverySessionRepository,
        command_repository: CommandRepository,
        edge_client: EdgeControllerClient,
    ) -> None:
        self._session_repository = session_repository
        self._send_command_use_case = SendCommandUseCase(
            repository=command_repository,
            edge_client=edge_client,
        )

    def execute(
        self, dto: StartDiscoveryInputDTO, *, created_by: str
    ) -> DiscoverySession:
        if not dto.edge_node_id:
            raise CommandValidationError("Edge node is required to start discovery.")

        session = self._session_repository.create(
            edge_node_id=dto.edge_node_id,
            started_by=created_by,
        )

        command = self._send_command_use_case.execute(
            SendCommandInputDTO(
                command_name=CommandType.DISCOVER.value,
                target_kind=CommandTargetKind.LOCATION.value,
                target_id=dto.edge_node_id,
                edge_node_id=dto.edge_node_id,
                payload={"session_id": session.id},
                idempotency_key=session.id,
            ),
            created_by=created_by,
        )

        self._session_repository.attach_command(
            session_id=session.id,
            command_id=str(command.id),
        )
        self._session_repository.mark_running(session_id=session.id)

        return session
