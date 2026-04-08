from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer
#from .tasks import send_welcome_email

class RegisterView(APIView):
    def post(self, request):
        s = RegisterSerializer(data=request.data)
        if s.is_valid():
            s.save()
            # 🔥 Trigger email using Celery
            #send_welcome_email.delay(user.email)
            return Response({'msg':'User Created'})
        return Response(s.errors)