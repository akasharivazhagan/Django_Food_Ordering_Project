from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Restaurant, Food
from .serializers import RestaurantSerializer, FoodSerializer

# 🔹 List all restaurants
class RestaurantListView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]


# 🔹 List foods based on restaurant
class FoodListView(ListAPIView):
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return Food.objects.filter(restaurant_id=restaurant_id)

    

#APIView (Manual):   


# class FoodListView(APIView):   
#   def get(self, request):        
#     foods = Food.objects.all()   
#     s = FoodSerializer(
#           foods, many=True)    
#     return Response(s.data) 