from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .tasks import process_order
from .models import Order, OrderItem
from food.models import Food

class CreateOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            food_id = request.data.get('food_id')
            food = get_object_or_404(Food, id=food_id)

            # ✅ Check existing PENDING order
            order = Order.objects.filter(user=request.user,status='PROCESSING').first()

            # ✅ If not exist → create new
            if not order:
                order = Order.objects.create(user=request.user,status='PROCESSING')

            # ✅ Add / update item
            item, created = OrderItem.objects.get_or_create(
                order=order,
                food=food,
                defaults={'quantity': 1}
            )

            if not created:
                item.quantity += 1
                item.save()

            # ✅ Calculate total
            total = sum(i.food.price * i.quantity for i in order.orderitem_set.all())
            order.total_price = total
            order.save()
            
            #send_order_email.delay(order.user.email, order.id, order.status)
            
            process_order.delay(order.id)

            return Response({
                "message": "Item added to cart",
                "order_id": order.id,
                "total": order.total_price,
                "status": order.status
            })

        except Exception as e:
            return Response({"error": str(e)}, status=400)
               
                
class Cart(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order = Order.objects.filter(user=request.user, status='PROCESSING').first()

        if not order:
            return Response({'items': [], 'total': 0})

        items = [
            {
                'food': i.food.name,
                'qty': i.quantity,
                'price': i.food.price
            }
            for i in order.orderitem_set.all()
        ]

        return Response({
            'items': items,
            'total': order.total_price
        })