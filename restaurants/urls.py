from django.urls import path
from .views import RestaurantListView, FoodListView
from .views import *

urlpatterns = [
    path('', RestaurantListView.as_view()),
    path('<int:restaurant_id>/foods/', FoodListView.as_view()),
    
      # 🍽️ Restaurant Admin CRUD
    path('admin/restaurants/', RestaurantAdminListView.as_view()),
    path('admin/restaurants/add/', RestaurantCreateView.as_view()),
    path('admin/restaurants/<int:pk>/', RestaurantDetailView.as_view()),
    path('admin/restaurants/<int:pk>/update/', RestaurantUpdateView.as_view()),
    path('admin/restaurants/<int:pk>/delete/', RestaurantDeleteView.as_view()),

    # 🍕 Food Admin CRUD
    path('admin/foods/', FoodAdminListView.as_view()),
    path('admin/foods/add/', FoodCreateView.as_view()),
    path('admin/foods/<int:pk>/', FoodDetailView.as_view()),
    path('admin/foods/<int:pk>/update/', FoodUpdateView.as_view()),
    path('admin/foods/<int:pk>/delete/', FoodDeleteView.as_view()),
]