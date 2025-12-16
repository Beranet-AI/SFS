from rest_framework.response import Response
from rest_framework.views import APIView


class LiveStatusListView(APIView):
    """
    Read-only view for current live status signals.
    In this iteration the data is derived externally, so we expose an empty list as a placeholder.
    """

    authentication_classes: list = []
    permission_classes: list = []

    def get(self, request):
        return Response([])
