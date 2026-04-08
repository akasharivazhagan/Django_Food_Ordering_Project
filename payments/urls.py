from django.urls import path
from .views import CreatePaymentView, VerifyPaymentView

urlpatterns = [
    path('create/<int:order_id>/', CreatePaymentView.as_view()),
    path('verify/', VerifyPaymentView.as_view()),
]