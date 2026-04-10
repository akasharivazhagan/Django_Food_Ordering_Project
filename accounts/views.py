from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer
#from .tasks import send_welcome_email

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,AdminRegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import AdminLoginSerializer


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User Registered Successfully"
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AdminRegisterView(APIView):

    def post(self, request):
        serializer = AdminRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Admin Registered Successfully"}, status=201)

        return Response(serializer.errors, status=400)
    
class AdminLoginView(TokenObtainPairView):
    serializer_class = AdminLoginSerializer