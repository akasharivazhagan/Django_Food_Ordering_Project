from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer

class RegisterView(APIView):
    def post(self, request):
        s = RegisterSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response({'msg':'User Created'})
        return Response(s.errors)