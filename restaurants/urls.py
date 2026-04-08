from django.urls import path
from .views import RestaurantListView, FoodListView

urlpatterns = [
    path('', RestaurantListView.as_view()),
    path('<int:restaurant_id>/foods/', FoodListView.as_view()),
]