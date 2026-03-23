from django.urls import path
from .views import FoodListView, FoodCreateView

urlpatterns = [
    path('', FoodListView.as_view()),
    path('add/', FoodCreateView.as_view()),
]