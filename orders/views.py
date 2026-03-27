from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItem
from food.models import Food

class AddToCart(APIView):
    def post(self, request):
        food = Food.objects.get(id=request.data['food_id'])

        # ✅ Only get PENDING order
        order = Order.objects.filter(user=request.user, status='PENDING').first()

        if not order:
            order = Order.objects.create(user=request.user)

        item = OrderItem.objects.filter(order=order, food=food).first()

        if item:
            item.quantity += 1
        else:
            item = OrderItem.objects.create(order=order, food=food, quantity=1)

        item.save()

        # total calculate
        total = sum(i.food.price * i.quantity for i in order.orderitem_set.all())
        order.total_price = total
        order.save()

        return Response({
            'order_id': order.id,
            'total': total
        })   
         

class Cart(APIView):
    def get(self, request):

        order = Order.objects.filter(user=request.user, status='PENDING').first()

        if not order:
            return Response({'items': [], 'total': 0})

        items = []

        for i in order.orderitem_set.all():
            items.append({
                'food': i.food.name,
                'qty': i.quantity,
                'price': i.food.price
            })

        return Response({
            'items': items,
            'total': order.total_price
        })