from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.events.application.services import EventService
from .serializers import EventSerializer


class EventListView(APIView):
    def get(self, request):
        service = EventService()
        events = service.list_events()
        data = [EventSerializer.from_entity(e) for e in events]
        return Response(data)


class EventAckView(APIView):
    def post(self, request, event_id: str):
        service = EventService()
        event = service.acknowledge(event_id)
        return Response(EventSerializer.from_entity(event))


class EventResolveView(APIView):
    def post(self, request, event_id: str):
        service = EventService()
        event = service.resolve(event_id)
        return Response(EventSerializer.from_entity(event))
