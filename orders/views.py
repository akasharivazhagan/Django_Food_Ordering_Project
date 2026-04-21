from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, AddToCartSerializer, OrderSerializer,CreateOrderSerializer,AddToCartResponseSerializer
from restaurants.models import Food,Restaurant
from .tasks import send_order_email
from rest_framework import status


# 🛒 Add to Cart
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)

        # ❌ Invalid input
        if not serializer.is_valid():
            return Response(
                {"message": "Invalid data", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        restaurant_id = serializer.validated_data['restaurant_id']
        food_id = serializer.validated_data['food_id']
        quantity = serializer.validated_data['quantity']

        # ✅ Safe fetch
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response(
                {"message": "Restaurant not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            food = Food.objects.get(id=food_id)
        except Food.DoesNotExist:
            return Response(
                {"message": "Food not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔥 Validate relationship
        if food.restaurant.id != restaurant.id:
            return Response(
                {"message": "Food not from selected restaurant"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🛒 Get/Create cart
        cart, _ = Cart.objects.get_or_create(
            user=request.user,
            restaurant=restaurant
        )

        # 🛒 Add / Update item
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            food=food
        )

        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity

        item.save()

        # ✅ Serializer response
        response_data = {
            "cart_id": cart.id,
            "food": food.name,
            "quantity": item.quantity
        }

        response_serializer = AddToCartResponseSerializer(response_data)

        return Response({
            "message": "Added to cart",
            "data": response_serializer.data
        }, status=status.HTTP_201_CREATED)


# 👀 View Cart
# class ViewCartView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         cart, _ = Cart.objects.get_or_create(user=request.user)
#         serializer = CartSerializer(cart)
#         return Response(serializer.data)
    
class ViewCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        carts = Cart.objects.filter(user=request.user)

        serializer = CartSerializer(carts, many=True)

        return Response(serializer.data)
    
# 📦 Create Order
class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)

        if serializer.is_valid():
            cart_id = serializer.validated_data['cart_id']

            cart = Cart.objects.get(id=cart_id, user=request.user)
            items = cart.items.all()

            total = 0

            order = Order.objects.create(
                user=request.user,
                cart=cart,
                total_amount=0
            )

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
            # items.delete()

            return Response({
                "message": "Order created",
                "order_id": order.id
            })

        return Response(serializer.errors)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# 📜 Order List
class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)