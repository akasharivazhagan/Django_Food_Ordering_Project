from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, AddToCartSerializer, OrderSerializer,CreateOrderSerializer
from restaurants.models import Food,Restaurant
from .tasks import send_order_email


# 🛒 Add to Cart
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)

        if serializer.is_valid():
            restaurant_id = serializer.validated_data['restaurant_id']
            food_id = serializer.validated_data['food_id']
            quantity = serializer.validated_data['quantity']

            restaurant = Restaurant.objects.get(id=restaurant_id)
            food = Food.objects.get(id=food_id)

            # 🔥 Ensure food belongs to selected restaurant
            if food.restaurant.id != restaurant.id:
                return Response({"error": "Food not from selected restaurant"})

            # 🛒 Get or create cart for that restaurant
            cart, _ = Cart.objects.get_or_create(
                user=request.user,
                restaurant=restaurant
            )

            item, created = CartItem.objects.get_or_create(
                cart=cart,
                food=food
            )

            if not created:
                item.quantity += quantity
            else:
                item.quantity = quantity

            item.save()

            return Response({
                "message": "Added to cart",
                "cart_id": cart.id
            })

        return Response(serializer.errors)

# 👀 View Cart
class ViewCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
class ViewCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        carts = Cart.objects.filter(user=request.user)

        data = []
        for cart in carts:
            items = cart.items.all()
            data.append({
                "cart_id": cart.id,
                "restaurant": cart.restaurant.name,
                "items": [
                    {
                        "food": item.food.name,
                        "quantity": item.quantity
                    } for item in items
                ]
            })

        return Response(data)   
    
    
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
            items.delete()

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