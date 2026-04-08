from django.urls import path
from .views import AddToCartView, ViewCartView, CreateOrderView, OrderListView

urlpatterns = [
    path('add-to-cart/', AddToCartView.as_view()),
    path('view-cart/', ViewCartView.as_view()),
    path('create-order/', CreateOrderView.as_view()),
    path('my-orders/', OrderListView.as_view()),
]