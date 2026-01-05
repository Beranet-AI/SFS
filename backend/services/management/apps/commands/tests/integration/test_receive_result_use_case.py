from datetime import datetime
from uuid import uuid4

from apps.commands.application.use_cases.receive_result.input_dto import (
    ReceiveResultInputDTO,
)
from apps.commands.application.use_cases.receive_result.use_case import (
    ReceiveResultUseCase,
)
from apps.commands.domain.entities.command import Command
from apps.commands.domain.entities.command_execution import CommandExecution
from apps.commands.domain.enums.command_status import CommandStatus
from apps.commands.domain.enums.command_type import CommandType
from apps.commands.domain.repositories.command_repository import CommandRepository


class FakeCommandRepository(CommandRepository):
    def __init__(self):
        self.command = Command(
            id="cmd-1",
            command_name=CommandType.GET_CONNECTED_DEVICES.value,
            target_kind="location",
            target_id="edge-1",
            edge_node_id="edge-1",
            payload={"scan_id": "scan-1"},
            idempotency_key="scan-1",
            status=CommandStatus.PENDING,
            source="manual",
            created_by="tester",
            created_at=datetime.utcnow(),
            ack_deadline_sec=10,
            result_deadline_sec=60,
            max_attempts=5,
        )
        self.scan_results = []

    def create(self, *, data: dict, created_by: str) -> Command:
        return self.command

    def get(self, *, command_id: str) -> Command:
        return self.command

    def mark_acked(self, *, command_id: str, meta: dict | None = None) -> Command:
        return self.command

    def mark_dispatched(self, *, command_id: str) -> Command:
        return self.command

    def mark_result(
        self,
        *,
        command_id: str,
        status: CommandStatus,
        result: dict | None = None,
        error_code: str = "",
        error_message: str = "",
    ) -> Command:
        return self.command

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
        self.scan_results.append((scan_id, device_uid, payload))


def test_receive_result_records_scan_results():
    repo = FakeCommandRepository()
    use_case = ReceiveResultUseCase(command_repository=repo)

    dto = ReceiveResultInputDTO(
        command_id="cmd-1",
        attempt_no=1,
        status="succeeded",
        result={
            "scan_id": "scan-1",
            "devices": [
                {"device_uid": "dev-1", "device_type": "sensor"},
                {"device_uid": "dev-2", "device_type": "sensor"},
            ],
        },
    )
    use_case.execute(dto)

    assert len(repo.scan_results) == 2
    assert repo.scan_results[0][0] == "scan-1"
