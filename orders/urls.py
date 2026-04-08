from django.urls import path
from .views import Cart,CreateOrder

urlpatterns = [
    path('add/', CreateOrder.as_view()),
    path('cart/', Cart.as_view()),
]