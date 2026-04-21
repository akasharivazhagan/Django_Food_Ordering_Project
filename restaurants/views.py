from rest_framework.permissions import IsAuthenticated
from .models import Restaurant, Food
from .serializers import RestaurantSerializer, FoodSerializer
from rest_framework.generics import (
    CreateAPIView, ListAPIView,
    RetrieveAPIView, UpdateAPIView, DestroyAPIView
)
from accounts.permissions import IsAdminUserCustom
from rest_framework import status
from rest_framework.response import Response


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
    
# ✅ CREATE Restaurant
class RestaurantCreateView(CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]


# 📜 LIST Restaurants (Admin view)
class RestaurantAdminListView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]


# 🔍 RETRIEVE Single Restaurant
class RestaurantDetailView(RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]


# ✏️ UPDATE Restaurant
class RestaurantUpdateView(UpdateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]


# ❌ DELETE Restaurant
class RestaurantDeleteView(DestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {
                "status": "success",
                "message": "Deleted successfully"
            },
            status=status.HTTP_200_OK
        )
    
    
    
    
    
# ✅ CREATE Food
class FoodCreateView(CreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]
    

# 📜 LIST Food (Admin)
class FoodAdminListView(ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]


# 🔍 RETRIEVE Food
class FoodDetailView(RetrieveAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]


# ✏️ UPDATE Food
class FoodUpdateView(UpdateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]


# ❌ DELETE Food
class FoodDeleteView(DestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {
                "status": "success",
                "message": "Deleted successfully"
            },
            status=status.HTTP_200_OK
        )

    

#APIView (Manual):   


# class FoodListView(APIView):   
#   def get(self, request):        
#     foods = Food.objects.all()   
#     s = FoodSerializer(
#           foods, many=True)    
#     return Response(s.data) 