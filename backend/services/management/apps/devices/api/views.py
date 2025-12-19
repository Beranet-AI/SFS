from rest_framework.views import APIView
from rest_framework.response import Response
from apps.devices.infrastructure.models.device_model import DeviceModel
from apps.devices.infrastructure.repositories.device_repo_impl import DjangoDeviceRepository
from apps.devices.application.use_cases.assign_device import AssignDeviceUseCase

class DevicesView(APIView):
    def get(self, request):
        qs = DeviceModel.objects.all().values(
            "id","serial","device_type","status","assigned_livestock_id"
        )
        return Response(list(qs))

class DeviceAssignView(APIView):
    repo = DjangoDeviceRepository()

    def post(self, request, device_id: str):
        livestock_id = request.data.get("livestock_id")
        uc = AssignDeviceUseCase(self.repo)
        device = uc.execute(device_id=device_id, livestock_id=livestock_id)
        return Response({
            "id": device.id,
            "assigned_livestock_id": device.assigned_livestock_id,
        })
