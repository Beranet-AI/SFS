# File: farm/api/base.py
from rest_framework.response import Response
from rest_framework.views import APIView

class BaseAPIView(APIView):
    def ok(self, data=None, status=200):
        return Response({"ok": True, "data": data}, status=status)
