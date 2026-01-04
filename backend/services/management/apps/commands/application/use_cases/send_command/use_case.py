from datetime import datetime
from typing import Protocol

from apps.commands.domain.domain_events.command_sent import CommandSent
from apps.commands.domain.domain_services.command_policy import CommandPolicy
from apps.commands.domain.repositories.command_repository import CommandRepository
from apps.commands.domain.specifications.can_send_command import CanSendCommand
from .input_dto import SendCommandInputDTO


class EventPublisher(Protocol):
    def publish(self, event: CommandSent) -> None:
        ...


class EdgeControllerClient(Protocol):
    def publish_command(self, *, edge_id: str, command: dict) -> None:
        ...


class NoopEventPublisher:
    def publish(self, event: CommandSent) -> None:
        return None


class SendCommandUseCase:
    def __init__(
        self,
        *,
        repository: CommandRepository,
        edge_client: EdgeControllerClient,
        event_publisher: EventPublisher | None = None,
    ) -> None:
        self._repository = repository
        self._edge_client = edge_client
        self._event_publisher = event_publisher or NoopEventPublisher()
        self._policy = CommandPolicy()
        self._specification = CanSendCommand()

    def execute(self, dto: SendCommandInputDTO, *, created_by: str):
        self._specification.validate(
            command_name=dto.command_name,
            target_kind=dto.target_kind,
            target_id=dto.target_id,
            payload=dto.payload,
            ack_deadline_sec=dto.ack_deadline_sec,
            result_deadline_sec=dto.result_deadline_sec,
            max_attempts=dto.max_attempts,
        )

        data = self._policy.apply(
            command_name=dto.command_name,
            target_kind=dto.target_kind,
            target_id=dto.target_id,
            edge_node_id=dto.edge_node_id,
            payload=dto.payload,
            idempotency_key=dto.idempotency_key,
            ack_deadline_sec=dto.ack_deadline_sec,
            result_deadline_sec=dto.result_deadline_sec,
            max_attempts=dto.max_attempts,
        )
        command = self._repository.create(data=data, created_by=created_by)
        edge_id = command.edge_node_id or command.target_id
        payload = {
            "command_id": str(command.id),
            "command_type": command.command_name,
            "edge_id": edge_id,
            "issued_at": command.created_at.isoformat(),
            "payload": command.payload,
        }
        self._edge_client.publish_command(edge_id=edge_id, command=payload)
        self._repository.mark_dispatched(command_id=command.id)
        event = CommandSent(
            command_id=command.id,
            command_name=command.command_name,
            target_kind=command.target_kind.value,
            target_id=command.target_id,
            payload=command.payload,
            occurred_at=datetime.utcnow(),
        )
        self._event_publisher.publish(event)
        return command
