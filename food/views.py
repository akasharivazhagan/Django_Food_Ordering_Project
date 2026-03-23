from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Food
from .serializers import FoodSerializer
from rest_framework.response import Response


#using generic view method
class FoodListView(ListAPIView): #GET
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

class FoodCreateView(CreateAPIView):  #POST
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    

#APIView (Manual):   


# class FoodListView(APIView):   
#   def get(self, request):        
#     foods = Food.objects.all()   
#     s = FoodSerializer(
#           foods, many=True)    
#     return Response(s.data) 