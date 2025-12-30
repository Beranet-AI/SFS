from apps.commands.application.services.command_api_service import (
    CommandApiService,
)
from .input_dto import ReceiveResultInputDTO


class ReceiveResultUseCase:

    def __init__(self, service: CommandApiService | None = None):
        self._service = service or CommandApiService()

    def execute(self, *, payload: dict):
        self._service.ingest_result(payload=payload)

    def report(self, dto: ReceiveResultInputDTO):
        self._service.report_result(data=dto.to_dict())
