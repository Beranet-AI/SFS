from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from devices.models import SensorReading  # اگر چنین مدلی وجود دارد
from devices.serializers import SensorReadingSerializer  # اگر serializer تعریف شده
from django.http import JsonResponse, Http404
from devices.models import Sensor

class SensorReadingView(APIView):
    def post(self, request):
        serializer = SensorReadingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def sensor_detail_view(request, pk):
    try:
        sensor = Sensor.objects.get(pk=pk)
        return JsonResponse({"id": sensor.id, "name": sensor.name})
    except Sensor.DoesNotExist:
        raise Http404("Sensor not found")
