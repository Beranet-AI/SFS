from datetime import datetime
from uuid import uuid4

from apps.commands.application.services.command_dispatcher import CommandDispatcher
from apps.commands.application.use_cases.send_command.input_dto import (
    SendCommandInputDTO,
)
from apps.commands.application.use_cases.send_command.use_case import (
    SendCommandUseCase,
)
from apps.commands.domain.entities.command import Command
from apps.commands.domain.entities.command_execution import CommandExecution
from apps.commands.domain.enums.command_status import CommandStatus
from apps.commands.domain.repositories.capability_repository import (
    CapabilityRepository,
    CommandCapability,
)
from apps.commands.domain.repositories.command_repository import CommandRepository


class FakeCommandRepository(CommandRepository):
    def __init__(self):
        self.commands = {}
        self.last_created = None
        self.dispatched = []

    def create(self, *, data: dict, created_by: str) -> Command:
        command_id = str(uuid4())
        command = Command(
            id=command_id,
            command_name=data["command_name"],
            target_kind=data["target_kind"],
            target_id=data["target_id"],
            edge_node_id=data["edge_node_id"],
            payload=data["payload"],
            idempotency_key=data["idempotency_key"],
            status=CommandStatus.PENDING,
            source="manual",
            created_by=created_by,
            created_at=datetime.utcnow(),
            ack_deadline_sec=data["ack_deadline_sec"],
            result_deadline_sec=data["result_deadline_sec"],
            max_attempts=data["max_attempts"],
        )
        self.commands[command_id] = command
        self.last_created = command
        return command

    def get(self, *, command_id: str) -> Command:
        return self.commands[command_id]

    def mark_acked(self, *, command_id: str, meta: dict | None = None) -> Command:
        return self.commands[command_id]

    def mark_dispatched(self, *, command_id: str) -> Command:
        self.dispatched.append(command_id)
        return self.commands[command_id]

    def mark_result(
        self,
        *,
        command_id: str,
        status: CommandStatus,
        result: dict | None = None,
        error_code: str = "",
        error_message: str = "",
    ) -> Command:
        return self.commands[command_id]

    def record_execution_ack(
        self,
        *,
        command_id: str,
        attempt_no: int,
        executor_receipt: str | None = None,
        meta: dict | None = None,
    ) -> CommandExecution:
        return CommandExecution(
            id=str(uuid4()),
            command_id=command_id,
            attempt_no=attempt_no,
            status="acked",
            created_at=datetime.utcnow(),
        )

    def record_execution_result(
        self,
        *,
        command_id: str,
        attempt_no: int,
        status: str,
        result: dict | None = None,
        error_code: str = "",
        error_message: str = "",
        meta: dict | None = None,
    ) -> CommandExecution:
        return CommandExecution(
            id=str(uuid4()),
            command_id=command_id,
            attempt_no=attempt_no,
            status=status,
            created_at=datetime.utcnow(),
        )

    def record_scan_result(
        self,
        *,
        scan_id: str,
        device_uid: str,
        payload: dict,
    ) -> None:
        return None


class FakeCapabilityRepository(CapabilityRepository):
    def list_capabilities(self) -> list[CommandCapability]:
        return []


class FakeExecutor:
    def __init__(self):
        self.commands = []

    def execute(self, *, edge_id: str, command: dict) -> None:
        self.commands.append((edge_id, command))


def test_send_command_dispatches():
    repo = FakeCommandRepository()
    executor = FakeExecutor()
    dispatcher = CommandDispatcher(
        edge_executor=executor,
        device_executor=executor,
        capability_repository=FakeCapabilityRepository(),
    )

    use_case = SendCommandUseCase(
        repository=repo,
        dispatcher=dispatcher,
        capability_repository=FakeCapabilityRepository(),
    )
    dto = SendCommandInputDTO(
        command_name="custom",
        target_kind="device",
        target_id="device-1",
    )

    output = use_case.execute(dto, created_by="tester")

    assert output.command_id in repo.commands
    assert repo.dispatched
    assert executor.commands
