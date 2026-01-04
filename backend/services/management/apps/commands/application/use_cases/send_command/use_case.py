from datetime import datetime
from typing import Protocol

from apps.commands.domain.domain_events.command_sent import CommandSent
from apps.commands.domain.domain_services.command_policy import CommandPolicy
from apps.commands.domain.repositories.command_repository import CommandRepository
from apps.commands.domain.specifications.can_send_command import CanSendCommand
from apps.commands.infrastructure.repositories.command_repo_impl import (
    DjangoCommandRepository,
)
from .input_dto import SendCommandInputDTO


class EventPublisher(Protocol):
    def publish(self, event: CommandSent) -> None:
        ...


class NoopEventPublisher:
    def publish(self, event: CommandSent) -> None:
        return None


class SendCommandUseCase:
    def __init__(
        self,
        repository: CommandRepository | None = None,
        event_publisher: EventPublisher | None = None,
    ) -> None:
        self._repository = repository or DjangoCommandRepository()
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
