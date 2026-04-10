from django.urls import path
from .views import AdminLoginView, RegisterView,AdminRegisterView
from rest_framework_simplejwt.views import TokenObtainPairView
from .admin_views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    
    path('admin/register/', AdminRegisterView.as_view()),
    path('admin/login/', AdminLoginView.as_view()),
    path('admin/users/', AllUsersView.as_view()),
    path('admin/orders/', AllOrdersView.as_view()),
    path('admin/payments/', AllPaymentsView.as_view()),
    path('admin/revenue/', RevenueView.as_view()),
    path('admin/order-count/', OrderCountView.as_view()),
    path('admin/top-restaurants/', TopRestaurantsView.as_view()),
]