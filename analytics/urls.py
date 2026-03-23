from django.urls import path
from .views import Analytics

urlpatterns = [
    path('', Analytics.as_view()),
]