from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from orders.models import Order

class Analytics(APIView):
    def get(self, request):
        return Response({
            'orders': Order.objects.count(),
            'sales': Order.objects.aggregate(Sum('total_price'))['total_price__sum']
        })