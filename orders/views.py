from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, AddToCartSerializer, OrderSerializer
from restaurants.models import Food
from .tasks import send_order_email


# 🛒 Add to Cart
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)

        if serializer.is_valid():
            food_id = serializer.validated_data['food_id']
            quantity = serializer.validated_data['quantity']

            food = Food.objects.get(id=food_id)

            cart, _ = Cart.objects.get_or_create(user=request.user)

            item, created = CartItem.objects.get_or_create(
                cart=cart, food=food
            )

            if not created:
                item.quantity += quantity
            else:
                item.quantity = quantity

            item.save()

            return Response({"message": "Added to cart"})

        return Response(serializer.errors)


# 👀 View Cart
class ViewCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


# 📦 Create Order
class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()

        total = 0

        order = Order.objects.create(user=request.user, total_amount=0)

        for item in items:
            total += item.food.price * item.quantity

            OrderItem.objects.create(
                order=order,
                food=item.food,
                quantity=item.quantity,
                price=item.food.price
            )

        order.total_amount = total
        order.save()
        
        send_order_email.delay(order.id)

        # clear cart
        items.delete()

        return Response({"message": "Order created", "order_id": order.id})


# 📜 Order List
class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)