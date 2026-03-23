from django.urls import path
from .views import AddToCart, Cart

urlpatterns = [
    path('add/', AddToCart.as_view()),
    path('cart/', Cart.as_view()),
]