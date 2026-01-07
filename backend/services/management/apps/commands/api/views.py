from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.commands.api.admin_views.dependencies import (
    build_receive_result_use_case,
)
from apps.commands.api.serializers import ReceiveResultSerializer
from apps.commands.application.use_cases.receive_result.input_dto import (
    ReceiveResultInputDTO,
)


@api_view(["POST"])
def receive_command_result_view(request):
    serializer = ReceiveResultSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    dto = ReceiveResultInputDTO(
        command_id=str(data["command_id"]),
        attempt_no=data["attempt_no"],
        status=data["status"],
        result=data.get("result") or {},
        error_code=data.get("error_code") or "",
        error_message=data.get("error_message") or "",
        meta=data.get("meta") or {},
    )

    use_case = build_receive_result_use_case()
    output = use_case.execute(dto)

    return Response(
        {"command_id": output.command_id, "status": output.status},
        status=status.HTTP_200_OK,
    )
