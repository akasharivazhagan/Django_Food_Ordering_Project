from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUserCustom
from orders.models import Order
from payments.models import Payment
from restaurants.models import Restaurant
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count

User = get_user_model()


# 👥 All Users
class AllUsersView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserCustom]

    def get(self, request):
        users = User.objects.all().values('id', 'email', 'username')
        return Response(users)


# 📦 All Orders
class AllOrdersView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserCustom]

    def get(self, request):
        orders = Order.objects.all().values()
        return Response(orders)


# 💳 All Payments
class AllPaymentsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserCustom]

    def get(self, request):
        payments = Payment.objects.all().values()
        return Response(payments)


# 💰 Total Revenue
class RevenueView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserCustom]

    def get(self, request):
        total = Order.objects.filter(status='completed').aggregate(total_revenue=Sum('total_amount'))
        return Response(total)


# 📊 Total Orders Count
class OrderCountView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserCustom]

    def get(self, request):
        count = Order.objects.count()
        return Response({"total_orders": count})


# 🍽️ Top Restaurants
class TopRestaurantsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserCustom]

    def get(self, request):
        data = (
            Order.objects.values('items__food__restaurant__name').annotate(total_orders=Count('id')).order_by('-total_orders')[:5]
        )
        return Response(data)