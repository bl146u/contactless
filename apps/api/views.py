from rest_framework.views import APIView
from rest_framework.response import Response


class ConfigAPIView(APIView):
    def get(self, request, **kwargs):
        return Response({})
